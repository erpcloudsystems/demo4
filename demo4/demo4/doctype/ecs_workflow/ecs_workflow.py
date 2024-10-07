# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model import no_value_fields
from frappe.model.document import Document



class ECSWorkFlow(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from frappe.workflow.doctype.workflow_document_state.workflow_document_state import (
			WorkflowDocumentState,
		)
		from frappe.workflow.doctype.workflow_transition.workflow_transition import ECSWorkflowTransition

		select_doctype: DF.Link
		is_active: DF.Check
		department: DF.Check
		branch: DF.Check
		designation: DF.Check
		states: DF.Table[WorkflowDocumentState]
		transition: DF.Table[ECSWorkflowTransition]

	# end: auto-generated types
	def validate(self):
		self.set_active()
		self.create_custom_field_for_workflow_state()
		self.update_default_workflow_status()
		self.validate_docstatus()

	def on_update(self):
		frappe.clear_cache(doctype=self.select_doctype)

	def create_custom_field_for_workflow_state(self):
		frappe.clear_cache(doctype=self.select_doctype)
		meta = frappe.get_meta(self.select_doctype)
		if not meta.get_field(self.workflow_state_field):
			# create custom field
			frappe.get_doc(
				{
					"doctype": "Custom Field",
					"dt": self.select_doctype,
					"__islocal": 1,
					"fieldname": self.workflow_state_field,
					"label": self.workflow_state_field.replace("_", " ").title(),
					"hidden": 1,
					"allow_on_submit": 1,
					"no_copy": 1,
					"fieldtype": "Link",
					"options": "Workflow State",
					"owner": "Administrator",
				}
			).save()

			frappe.msgprint(
				_("Created Custom Field {0} in {1}").format(self.workflow_state_field, self.select_doctype)
			)

	def update_default_workflow_status(self):
		docstatus_map = {}
		states = self.get("states")
		for d in states:
			if d.doc_status not in docstatus_map:
				frappe.db.sql(
					f"""
					UPDATE `tab{self.select_doctype}`
					SET `{self.workflow_state_field}` = %s
					WHERE ifnull(`{self.workflow_state_field}`, '') = ''
					AND `docstatus` = %s
				""",
					(d.state, d.doc_status),
				)

				docstatus_map[d.doc_status] = d.state

	def validate_docstatus(self):
		def get_state(state):
			for s in self.states:
				if s.state == state:
					return s

			frappe.throw(frappe._("{0} not a valid State").format(state))

		for t in self.transitions:
			state = get_state(t.state)
			next_state = get_state(t.next_state)

			if state.doc_status == "2":
				frappe.throw(
					frappe._("Cannot change state of Cancelled Document. Transition row {0}").format(t.idx)
				)

			if state.doc_status == "1" and next_state.doc_status == "0":
				frappe.throw(
					frappe._(
						"Submitted Document cannot be converted back to draft. Transition row {0}"
					).format(t.idx)
				)

			if state.doc_status == "0" and next_state.doc_status == "2":
				frappe.throw(frappe._("Cannot cancel before submitting. See Transition {0}").format(t.idx))

	def set_active(self):
		if int(self.is_active or 0):
			# clear all other
			frappe.db.sql(
				"""UPDATE `tabECS Workflow` SET `is_active`=0
				WHERE `select_doctype`=%s""",
				self.select_doctype,
			)


@frappe.whitelist()
def get_workflow_state_count(doctype, workflow_state_field, states):
	frappe.has_permission(doctype=doctype, ptype="read", throw=True)
	states = frappe.parse_json(states)

	if workflow_state_field in frappe.get_meta(doctype).get_valid_columns():
		result = frappe.get_all(
			doctype,
			fields=[workflow_state_field, "count(*) as count"],
			filters={workflow_state_field: ["not in", states]},
			group_by=workflow_state_field,
		)
		return [r for r in result if r[workflow_state_field]]