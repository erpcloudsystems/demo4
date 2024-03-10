from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
	pass
@frappe.whitelist()
def after_insert(doc, method=None):
	pass
@frappe.whitelist()
def onload(doc, method=None):
	pass
@frappe.whitelist()
def before_validate(doc, method=None):
	pass
@frappe.whitelist()
def validate(doc, method=None):
	if doc.custom_warehouse:
		for row in doc.custom_consumed_items_table:
			if row.consumed_quantity is None:
				row.consumed_quantity = 0
			if float(row.consumed_quantity) < 1:
				frappe.throw("Row #" + str(row.idx) + ": Please Enter The Consumed Quantity Of Item Code " + str(row.item_code))
			if not frappe.db.exists("Bin", {"warehouse": doc.custom_warehouse, "item_code": row.item_code}):
				row.valuation_rate = 0
			else:
				row.valuation_rate = frappe.db.get_value("Bin", {"warehouse": doc.custom_warehouse, "item_code": row.item_code}, "valuation_rate")
			row.total_value = row.valuation_rate * float(row.consumed_quantity)
		
@frappe.whitelist()
def on_submit(doc, method=None):
	stock_entry = frappe.get_doc({
		"doctype": "Stock Entry",
		"stock_entry_type": "Material Issue",
		"from_warehouse": doc.custom_warehouse,
	})
	for row in doc.custom_consumed_items_table:
		item = stock_entry.append("items", {})
		item.item_code = row.item_code
		item.s_warehouse = doc.custom_warehouse
		item.qty = row.consumed_quantity
		if frappe.db.exists("Item Default", {"parent": row.item_code}):
			item.expense_account = frappe.db.get_value("Item Default", {"parent": row.item_code}, "expense_account")
		
	stock_entry.insert()
	stock_entry.submit()
	doc.custom_stock_entry = stock_entry.name


	# asset_repair = frappe.get_doc({
	# 	"doctype": "Asset Repair",
	# 	"asset": doc.asset_maintenance,
	# 	"asset_name": doc.asset_name,
	# 	"failure_date": doc.completion_date,
	# 	"completion_date": doc.completion_date,
	# 	"repair_status": "Completed",
	# 	"stock_consumption": 1,
	# 	"repair_cost": 0,
	# 	"warehouse": doc.custom_warehouse,
	# 	"description": doc.name + ": " +doc.task_name,
	# 	"actions_performed": doc.actions_performed,
	# })
	# for row in doc.custom_consumed_items_table:
	# 	item = asset_repair.append("stock_items", {})
	# 	item.item_code = row.item_code
	# 	item.valuation_rate = row.valuation_rate
	# 	item.consumed_quantity = row.consumed_quantity
	# 	item.serial_and_batch_bundle = row.serial_and_batch_bundle
		
	# asset_repair.insert()
	# asset_repair.submit()

@frappe.whitelist()
def on_cancel(doc, method=None):
	if doc.custom_stock_entry:
		stock_entry = frappe.get_doc("Stock Entry", doc.custom_stock_entry)
		stock_entry.cancel()
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
	pass
@frappe.whitelist()
def before_save(doc, method=None):
	pass
@frappe.whitelist()
def before_cancel(doc, method=None):
	pass
@frappe.whitelist()
def on_update(doc, method=None):
	pass