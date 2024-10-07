import frappe
from frappe import _
from frappe.desk.notifications import clear_doctype_notifications

from frappe.workflow.doctype.workflow_action.workflow_action import send_workflow_action_email

from frappe.model.workflow import (
    get_workflow_name,
    send_email_alert,
)

from frappe.utils.background_jobs import enqueue

from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
    clear_workflow_actions,
    is_workflow_action_already_created,
    update_completed_workflow_actions,
    get_next_possible_transitions,
    create_workflow_actions_for_roles,
)

from .permission import (
    is_active_user,
    check_user_have_branch,
    check_user_have_custom_designation,
    check_user_have_custom_department,
    check_user_have_custom_company,
)

from .send_emails import send_emails

from frappe.model.workflow import (
    get_workflow_name,
)

from datetime import datetime, timedelta

# Check if the current user has the role 'System Admin'
def is_system_admin(user):
    users = frappe.db.sql(f"""
        SELECT u.name FROM `tabUser` u
        JOIN `tabHas Role` hr on hr.parent = u.name
        WHERE role = 'System Admin'
    """, as_dict = True)
    
    if user in users:
        return True
    
    return False


# Check if the current user can proceed with the workflow action
def can_process_workflow_action(doc):
    data = []
    
    try:
        # Get the current and next workflow state
        next_state = get_doc_workflow_state(doc)
        current_state = doc.get('custom_current_state')
        workflow = get_workflow_name(doc.get("doctype"))

        # if the next state is 'Cancelled' change the current state to 'Approved'
        if next_state == 'Cancelled':
            current_state = 'Approved'

        # set the condition to get workflow transition based on current and next state
        condition = f"AND state = '{current_state}' AND next_state = '{next_state}'"

        # Query the workflow transition based on the current and next states
        query = frappe.db.sql(f"""
            SELECT * FROM `tabWorkflow Transition` wt
            WHERE wt.parent = %s {condition}
        """, (workflow,), as_dict=True)

        if query:
            data = query[0]
            data['modified'] = doc.custom_modified

        # Update state and modified date if states differ to prevent recursion
        if current_state != next_state and next_state != 'Cancelled':
            doc.custom_current_state = next_state
            doc.custom_modified = datetime.now()
            send_emails(doc, next_state)
            doc.save()
    
    except Exception as e:
        frappe.msgprint(f"Error processing workflow actions: {str(e)}")
    
    # get the current user
    user = frappe.session.user

    # Check if the user is a system admin
    if is_system_admin(user):
        return
    
    if data:
        modified_time = data['modified']
        
        # Check if modified_time is a string, convert it to datetime
        if isinstance(modified_time, str):
            modified_time = datetime.strptime(modified_time, '%Y-%m-%d %H:%M:%S.%f')
                
        current_time = datetime.now()  # Get current time in UTC
        
        # if difference between the current and last modified time is larger than specific time ignore all restriction except role
        if data['custom_open_after_hours']:
            try:
                data['custom_open_after_hours'] = int(data['custom_open_after_hours'])
                if current_time - modified_time >= timedelta(hours = data['custom_open_after_hours']):
                    return
            except ValueError:
                frappe.msgprint("The value provided is not a valid integer.")
        # else:
            # frappe.msgprint('No time is set for this action.')
 
    # Check various conditions based on user properties and workflow requirements
    if data and data['custom_user'] and data['custom_user'] != user and is_active_user(doc):
        frappe.throw(f"Only user '{data['custom_user']}' can proceed with this action.")

    if data and data['custom_branch'] and not check_user_have_branch(doc, user, data['custom_branch']):
        frappe.throw(f"Current user must have branch '{data['custom_branch']}' to proceed with this action.")

    if data and data['custom_designation'] and not check_user_have_custom_designation(doc, user, data['custom_designation']):
        frappe.throw(f"Current user must have the designation '{data['custom_designation']}' to proceed with this action.")

    if data and data['custom_department'] and not check_user_have_custom_department(doc, user, data['custom_department']):
        frappe.throw(f"Current user must be in the department '{data['custom_department']}' to proceed with this action.")

    if data and data['custom_company'] and not check_user_have_custom_company(doc, user, data['custom_company']):
        frappe.throw(f"Current user must be in the company '{data['custom_company']}' to proceed with this action.")


# Custom process workflow actions based on user permissions and workflow conditions
def custom_process_workflow_actions(doc, state): 
    frappe.msgprint('55') 

    # # if the current user doesn't have the permission to continue throw an error 
    # can_process_workflow_action(doc)
        
    # workflow = get_workflow_name(doc.get("doctype"))
    # if not workflow:
    #     return

    # if state == "on_trash":
    #     clear_workflow_actions(doc.get("doctype"), doc.get("name"))
    #     return

    # if is_workflow_action_already_created(doc):
    #     return

    # update_completed_workflow_actions(doc, workflow=workflow, workflow_state=get_doc_workflow_state(doc))
    # clear_doctype_notifications("Workflow Action")

    # next_possible_transitions = get_next_possible_transitions(workflow, get_doc_workflow_state(doc), doc)

    # if not next_possible_transitions:
    #     return

    # roles = {t.allowed for t in next_possible_transitions}
    # create_workflow_actions_for_roles(roles, doc)

    # if send_email_alert(workflow):
    #     enqueue(
    #         send_workflow_action_email,
    #         queue="short",
    #         doc=doc,
    #         transitions=next_possible_transitions,
    #         enqueue_after_commit=True,
    #         now=frappe.flags.in_test,
    #     )