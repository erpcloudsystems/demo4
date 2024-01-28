// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Product inquiry"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80"
		},

		{
			"fieldname":"party_name",
			"label": __("Lead"),
			"fieldtype": "Link",
			"options" : "Lead",
			"reqd": 0
		},
		{
			"fieldname":"item_code",
			"label": __("item_code"),
			"fieldtype": "Link",
			"options" : "Item",
			"reqd": 0
		},
	]
};
