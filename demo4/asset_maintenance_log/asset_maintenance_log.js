// frappe.ui.form.on("Asset Maintenance Log", "validate", function (frm) {
//     $.each(frm.doc.custom_consumed_items_table || [], function(i, d) {
//         frappe.call({
//             'method': 'frappe.client.get_value',
//             'args': {
//                 'doctype': 'Bin',
//                 'fieldname': 'valuation_rate',
//                 'filters': {
//                     'item_code': d.item_code,
//                     'warehouse': frm.doc.custom_warehouse,
//                 }
//             },
//             callback: function(r){
//                 d.valuation_rate = r.message.valuation_rate;
//                 console.log(r.message.valutation_rate)
//             }
//         });
//     });
// });


// frappe.ui.form.on("Asset Repair Consumed Item", "item_code", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
//     frappe.db.get_value("Bin", {"item_code": d.item_code, "warehouse": frm.doc.custom_warehouse }, "valuation_rate",
//     function(value) {
//     d.valuation_rate = value.valuation_rate;
//     });
//     });