import frappe
from frappe import _
import time
import subprocess

from .permission import (
    is_active_user,
    check_user_have_branch,
    check_user_have_custom_designation,
    check_user_have_custom_department,
    check_user_have_custom_company,
)

# Function to start a single worker process for a given queue
def start_worker(queue_name='short'):
    command = ['bench', 'worker', '--queue', queue_name]
    subprocess.Popen(command)

# Function to start multiple worker processes for a given queue
def start_multiple_workers(num_workers, queue_name='short'):
    for _ in range(num_workers):
        start_worker(queue_name)

# Function to send an email to a users based on a workflow action
def send_email_to_user(user, action, doc):
    current_state = doc.custom_current_state
    email_subject = f"Workflow Action: {doc.get('name')} requires your attention"
    email_content = f"""
        Dear {user},<br><br>
        
        A workflow action for {doc.get('doctype')} {doc.get('name')} is now '{current_state}'.<br>
        The available action you can take is: '{action}'.<br><br>
        
        Please review and take the necessary action.
        
        Thank you.
    """

    frappe.sendmail(
        recipients=user,
        subject=email_subject,
        message=email_content,
    )

# Function to send an email to a user after a delay if the state remains unchanged
def send_email_to_user2(user, action, doc, delay_in_seconds):
    initial_state = doc.custom_current_state
    
    # Delay for the specified amount of time
    time.sleep(delay_in_seconds)
    
    current_doc = frappe.get_doc(doc.get('doctype'), doc.get('name'))
    current_state = current_doc.custom_current_state

    # if the state remains unchanged send the email
    if current_state == initial_state:
        send_email_to_user(user, action, current_doc)

# Function to enqueue email tasks and start workers if needed
def schedule_email(user, action, doc, delay_in_seconds, num_workers=1):
    try:
        # Start additional workers
        start_multiple_workers(num_workers, 'short')
        
        # Enqueue the email task
        frappe.enqueue(
            send_email_to_user2,  
            queue='short',  
            timeout=2592000,
            job_name=f"Email to {user}",
            user=user,
            action=action,
            doc=doc,
            delay_in_seconds=delay_in_seconds,
            enqueue_after_commit=True, 
        )
    except Exception as e:
        frappe.msgprint(f"Error scheduling email: {str(e)}")

# Function to get users with a specific role
def get_users_with_specific_role(role):
    users = frappe.db.sql(f"""
        SELECT u.name FROM `tabUser` u
        JOIN `tabHas Role` hr on hr.parent = u.name
        WHERE role = %s
    """, (role,), as_dict = True)

    return [user.name for user in users]

# Function to send workflow action emails to relevant users
def send_workflow_action_email(doc, current_state):
    doctype = doc.get("doctype")

    condition = f"AND state = '{current_state}'"

    query = frappe.db.sql(f"""
        SELECT * FROM `tabWorkflow Transition` wt
        WHERE wt.parent = %s {condition}
    """, (doctype,), as_dict=True)

    users = []
    schedule_users = []

    for field in query:
        selected_users = get_users_with_specific_role(field['allowed'])

        for user in selected_users:
            take_user = True
            if field and field['custom_user'] and field['custom_user'] != user and is_active_user(doc):
                take_user = False
            if field and field['custom_branch'] and not check_user_have_branch(doc, user, field['custom_branch']):
                take_user = False
            if field and field['custom_designation'] and not check_user_have_custom_designation(doc, user, field['custom_designation']):
                take_user = False
            if field and field['custom_department'] and not check_user_have_custom_department(doc, user, field['custom_department']):
                take_user = False
            if field and field['custom_company'] and not check_user_have_custom_company(doc, user, field['custom_company']):
                take_user = False

            # users that could make actions on the workflow immediately
            if take_user:
                users.append({
                    'user': user,
                    'action': field['action'],
                })
            #   users that could make actions on the workflow after a delay
            elif field and field['custom_open_after_hours']:
                schedule_users.append({
                    'user': user,
                    'action': field['action'],
                    'delay': field['custom_open_after_hours']
                })

    schedule_users = list({tuple(sorted(d.items())): d for d in schedule_users}.values())
    users = list({tuple(sorted(d.items())): d for d in users}.values())

    for user in users:
        send_email_to_user(user['user'], user['action'], doc)

    for user in schedule_users:
        delay_in_seconds = int(user['delay']) * 60 * 60
        schedule_email(user['user'], user['action'], doc, delay_in_seconds)

# if send emails checkbox is active send workflow action emails to users otherwise do nothing
def send_emails(doc, current_state):
    send = frappe.db.sql("""
        SELECT custom_send_emails FROM `tabWorkflow`
        WHERE name = %s
    """, doc.get("doctype"), as_dict = True)
    
    if send[0]['custom_send_emails']:
        send_workflow_action_email(doc, current_state)