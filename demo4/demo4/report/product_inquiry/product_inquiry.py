# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters, columns)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Lead"),
			"fieldname": "party_name",
			"fieldtype": "Link",
			"options": "Lead",
			"width": 180
		},
		{
			"label": _("Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Date"),
			"fieldname": "transaction_date",
			"fieldtype": "Date",
			"width": 180
		},
		{
			"label": _("phone no"),
			"fieldname": "contact_mobile",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("item_code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 180
		},

		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 180
		}



	]


def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data


def get_item_price_qty_data(filters):
	conditions = ""
	conditions2 = ""
	if filters.get("from_date"):
		conditions += " and `tabOpportunity`.transaction_date >=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and `tabOpportunity`.transaction_date <=%(to_date)s"
	if filters.get("item_code"):
		conditions += " and `tabOpportunity Item`.item_code =%(item_code)s"
	
	result = []

	item_results = frappe.db.sql("""
			select 
					`tabOpportunity`.party_name as party_name,
					`tabOpportunity`.customer_name as customer_name,
					`tabOpportunity`.transaction_date as transaction_date,
					`tabOpportunity`.contact_mobile as contact_mobile,
					`tabOpportunity Item`.item_code as item_code,		
					`tabOpportunity Item`.item_name as item_name		
					
					
					
			from
			       `tabOpportunity` join  `tabOpportunity Item` on `tabOpportunity`.name = `tabOpportunity Item`.parent
			where
			  
			   `tabOpportunity`.status = "Open" 
			 {conditions}
			 
			""".format(conditions=conditions), filters, as_dict=1)

	if item_results:
		for item_dict in item_results:
			data = {
				'party_name': item_dict.party_name,
				'customer_name': _(item_dict.customer_name),
				'transaction_date': item_dict.transaction_date,
				'contact_mobile': _(item_dict.contact_mobile),
				'item_code': _(item_dict.item_code),
				'item_name': _(item_dict.item_name)

			}
			result.append(data)

	return result