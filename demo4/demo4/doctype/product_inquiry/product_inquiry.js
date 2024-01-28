// frappe.ui.form.on("Product Inquiry", {
//     send_whats_app_msg: function(frm, cdt, cdn) {
//         // Initialize arabicText
//         var arabicText = "";

//         frm.doc.product_inquiry_table.forEach(function(product_inquiry_table) {
//             arabicText += product_inquiry_table.item_name + "\n";
//             arabicText += product_inquiry_table.customer_name + "\n";
//         });

//         arabicText += "تشرفنا بخدمتكم 🌹";

//         // Replace "YOUR_PHONE_NUMBER" with the actual phone number
//         var phoneNumber = "YOUR_PHONE_NUMBER";
        
//         // Construct the WhatsApp API URL
//         var whatsappApiUrl = "https://api.whatsapp.com/send/?phone=" + phoneNumber + "&text=" + encodeURIComponent(arabicText);

//         // Open a new window or tab with the WhatsApp API URL
//         var myWin = window.open(whatsappApiUrl, "_blank");
//     }
// });
