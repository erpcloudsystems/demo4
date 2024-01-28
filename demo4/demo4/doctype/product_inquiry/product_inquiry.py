# demo4/demo4/doctype/product_inquiry/product_inquiry.py

import frappe
from frappe.model.document import Document

class ProductInquiry(Document):
    @frappe.whitelist()
    def validate(self, method=None):
        # Query Opportunities between the selected date range
        opportunities = frappe.get_all(
            "Opportunity",
            filters={
                "transaction_date": ["between", [self.from_date, self.to_date]],
            },
            fields=["name", "party_name", "customer_name", "contact_mobile","transaction_date"],
        )
        del self.product_inquiry_table[:]

        # Iterate through each Opportunity and fetch items
        for opportunity in opportunities:
            opportunity_name = opportunity.get("name")
            items = frappe.get_all(
                "Opportunity Item",
                filters={"parent": opportunity_name},
                fields=["item_code", "item_name"],
            )

            # Update Product Inquiry Table with Opportunity and Item data
            self.update_product_inquiry_table(opportunity, items)

    def update_product_inquiry_table(self, opportunity, items):
        # Your logic to update the product_inquiry_table here
        # You can use frappe.append to update the child table
        # For example:
        for item in items:
            row = self.append("product_inquiry_table", {
                "opportunity": opportunity.get("name"),
                "party_name": opportunity.get("party_name"),
                "contact_mobile": opportunity.get("contact_mobile"),
                "customer_name": opportunity.get("customer_name"),
                "date": opportunity.get("transaction_date"),
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
            })

        # Save the changes to the document
