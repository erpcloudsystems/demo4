from . import __version__ as app_version

app_name = "demo4"
app_title = "demo4"
app_publisher = "erpcloudsystems"
app_description = "demo4"
app_email = " "
app_license = "MIT"

doc_events = {
	"Asset Maintenance Log": {
		"before_insert": "demo4.asset_maintenance_log.asset_maintenance_log.before_insert",
		"after_insert": "demo4.asset_maintenance_log.asset_maintenance_log.after_insert",
		"onload": "demo4.asset_maintenance_log.asset_maintenance_log.onload",
		"before_validate": "demo4.asset_maintenance_log.asset_maintenance_log.before_validate",
		"validate": "demo4.asset_maintenance_log.asset_maintenance_log.validate",
		"on_submit": "demo4.asset_maintenance_log.asset_maintenance_log.on_submit",
		"on_cancel": "demo4.asset_maintenance_log.asset_maintenance_log.on_cancel",
		"on_update_after_submit": "demo4.asset_maintenance_log.asset_maintenance_log.on_update_after_submit",
		"before_save": "demo4.asset_maintenance_log.asset_maintenance_log.before_save",
		"before_cancel": "demo4.asset_maintenance_log.asset_maintenance_log.before_cancel",
		"on_update": "demo4.asset_maintenance_log.asset_maintenance_log.on_update",
	},
	
}
doctype_js = {
	"Asset Maintenance Log" : "asset_maintenance_log/asset_maintenance_log.js",
}
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/demo4/css/demo4.css"
# app_include_js = "/assets/demo4/js/demo4.js"

# include js, css files in header of web template
# web_include_css = "/assets/demo4/css/demo4.css"
# web_include_js = "/assets/demo4/js/demo4.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "demo4/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "demo4.utils.jinja_methods",
#	"filters": "demo4.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "demo4.install.before_install"
# after_install = "demo4.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "demo4.uninstall.before_uninstall"
# after_uninstall = "demo4.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "demo4.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"Workflow Action": "demo4.overrides.CustomWorkflowAction"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"demo4.scheduler_events.all.all"
	],
	"daily": [
		"demo4.scheduler_events.daily.daily"
	],
	"hourly": [
		"demo4.scheduler_events.hourly.hourly"
	],
	"weekly": [
		"demo4.scheduler_events.weekly.weekly"
	],
	"monthly": [
		"demo4.scheduler_events.monthly.monthly"
	],
}

# Testing
# -------

# before_tests = "demo4.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "demo4.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "demo4.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["demo4.utils.before_request"]
# after_request = ["demo4.utils.after_request"]

# Job Events
# ----------
# before_job = ["demo4.utils.before_job"]
# after_job = ["demo4.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"demo4.auth.validate"
# ]


# from frappe.utils import get_url
# url = get_url()
# if url == "https://demo4.erpcloud.systems":
# 	from frappe.workflow.doctype.workflow_action.workflow_action import process_workflow_actions 
# 	from demo4.overrides.workflowaction import custom_process_workflow_actions


# 	process_workflow_actions = custom_process_workflow_actions