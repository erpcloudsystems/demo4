import frappe
from frappe import _

# Check if the current user has the specific branch to proceed with the workflow action
def check_user_have_branch(doc, user, current_branch):
    doctype = doc.get("doctype")
    
    # Check if 'branch' is active in the workflow for the given doctype
    is_active = frappe.db.sql("""
        SELECT custom_branch FROM `tabWorkflow`
        WHERE name = %s
    """, (doctype), as_dict=True)

    # If 'branch' is not active, return True and proceed without checking
    if not is_active or (is_active and not is_active[0]['custom_branch']):
        return True

    # Get all branches the user has permission for
    all_user_branches = frappe.db.sql("""
        SELECT for_value FROM `tabUser Permission`
        WHERE allow = 'Branch' and user = %s
        """, (user), as_dict=True)

    # Get the branch associated with the employee's user ID
    employee_branch = frappe.db.sql("""
        SELECT branch FROM `tabEmployee`
        WHERE user_id = %s
        """, (user), as_dict=True)

    # Add the employee's branch to the list of user branches
    for branch in employee_branch:
        all_user_branches.append({'for_value': branch['branch']})

    # Check if the current branch is in the list of user branches
    proceed = False
    for user_branch in all_user_branches:
        if user_branch['for_value'] == current_branch:
            proceed = True

    # If the user has the current branch, return true otherwise return false 
    return proceed


# Check if the current user has the specific designation to proceed with the workflow action
def check_user_have_custom_designation(doc, user, current_designation):
    doctype = doc.get("doctype")
    
    # Check if custom_designation is active in the workflow for the given doctype
    is_active = frappe.db.sql("""
        SELECT custom_designation FROM `tabWorkflow`
        WHERE name = %s
    """, (doctype), as_dict=True)

    # If 'designation' is not active, return True and proceed without checking
    if not is_active or (is_active and not is_active[0]['custom_designation']):
        return True
    
    # Get all designations the user has permission for
    all_user_designation = frappe.db.sql("""
        SELECT for_value FROM `tabUser Permission`
        WHERE allow = 'Designation' and user = %s
        """, (user), as_dict=True)

    # Get the designation associated with the employee's user ID
    employee_designation = frappe.db.sql("""
        SELECT designation FROM `tabEmployee`
        WHERE user_id = %s
        """, (user), as_dict=True)

    # Add the employee's designation to the list of user designations
    for designation in employee_designation:
        all_user_designation.append({'for_value': designation['designation']})

    # Check if the current designation is in the list of user designations
    proceed = False
    for user_branch in all_user_designation:
        if user_branch['for_value'] == current_designation:
            proceed = True

    # If the user has the current designation, return true otherwise return false 
    return proceed


# Check if the current user has the specific department to proceed with the workflow action
def check_user_have_custom_department(doc, user, current_department):
    doctype = doc.get("doctype")
    
    # Check if custom_department is active in the workflow for the given doctype
    is_active = frappe.db.sql("""
        SELECT custom_department FROM `tabWorkflow`
        WHERE name = %s
    """, (doctype), as_dict=True)

    # If 'department' is not active, return True and proceed without checking
    if not is_active or (is_active and not is_active[0]['custom_department']):
        return True
    
    # Get all departments the user has permission for
    all_user_department = frappe.db.sql("""
        SELECT for_value FROM `tabUser Permission`
        WHERE allow = 'Department' and user = %s
        """, (user), as_dict=True)

    # Get the department associated with the employee's user ID
    employee_department = frappe.db.sql("""
        SELECT department FROM `tabEmployee`
        WHERE user_id = %s
        """, (user), as_dict=True)

    # Add the employee's department to the list of user departments
    for department in employee_department:
        all_user_department.append({'for_value': department['department']})

    # Check if the current department is in the list of user departments
    proceed = False
    for user_branch in all_user_department:
        if user_branch['for_value'] == current_department:
            proceed = True

    # If the user has the current department, return true otherwise return false 
    return proceed


# Check if the current user has the specific company to proceed with the workflow action
def check_user_have_custom_company(doc, user, current_company):
    doctype = doc.get("doctype")
    
    # Check if custom_company is active in the workflow for the given doctype
    is_active = frappe.db.sql("""
        SELECT custom_company FROM `tabWorkflow`
        WHERE name = %s
    """, (doctype), as_dict=True)

    # If 'company' is not active, return True and proceed without checking
    if not is_active or (is_active and not is_active[0]['custom_company']):
        return True
    
    # Get all companies the user has permission for
    all_user_companies = frappe.db.sql("""
        SELECT for_value FROM `tabUser Permission`
        WHERE allow = 'Company' and user = %s
        """, (user), as_dict=True)

    # Get the company associated with the employee's user ID
    employee_company = frappe.db.sql("""
        SELECT company FROM `tabEmployee`
        WHERE user_id = %s
        """, (user), as_dict=True)

    # Add the employee's company to the list of user companies
    for company in employee_company:
        all_user_companies.append({'for_value': company['company']})

    # Check if the current company is in the list of user companies
    proceed = False
    for user_branch in all_user_companies:
        if user_branch['for_value'] == current_company:
            proceed = True

    # If the user has the current company, return true otherwise return false 
    return proceed


# Check if checkbox 'user' is active
def is_active_user(doc):
    doctype = doc.get("doctype")
    
    # Check if custom_user is active in the workflow for the given doctype
    is_active = frappe.db.sql("""
        SELECT custom_user FROM `tabWorkflow`
        WHERE name = %s
    """, (doctype), as_dict=True)

    # If checkbox 'user' is active, return True otherwise return false
    if not is_active or (is_active and is_active[0]['custom_user']):
        return True
    return False