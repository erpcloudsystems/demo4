// Mapping of English numbers to Arabic numbers
const englishToArabicNumbers = {
    '0': '٠',
    '1': '١',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '٧',
    '8': '٨',
    '9': '٩'
};

frappe.ui.form.on('lab sample', {
    validate: function(frm) {
        // Function to convert English numbers to Arabic numbers within text content
        function convertNumbersToArabic(text) {
            return text.replace(/\d/g, (d) => englishToArabicNumbers[d]);
        }

        // Function to recursively convert numbers in text nodes of an HTML element
        function convertNumbersInHtml(html) {
            const div = document.createElement('div');
            div.innerHTML = html;

            function traverse(element) {
                if (element.nodeType === Node.TEXT_NODE) {
                    element.nodeValue = convertNumbersToArabic(element.nodeValue);
                } else if (element.nodeType === Node.ELEMENT_NODE) {
                    for (let child of element.childNodes) {
                        traverse(child);
                    }
                }
            }

            traverse(div);
            return div.innerHTML;
        }

        // Get the current HTML content of the lab_title field
        let labTitleHtml = frm.doc.report_title || '';

        // Convert numbers in the HTML content
        let convertedHtml = convertNumbersInHtml(labTitleHtml);

        // Set the converted HTML content back to the lab_title field
        frm.set_value('report_title', convertedHtml);
    }
});

// hide the print icon button embedded default in the form
frappe.ui.form.on("lab sample", {
    onload: function (frm) {
        $('button[data-original-title="Print"]').hide();
    },
    refresh: function (frm) {
        $('button[data-original-title="Print"]').hide();
    }
});


// frappe.ui.form.on("lab sample", {
//     validate: function (frm) {
//         if (!frm.is_new()) { 
//             frm.add_custom_button(__("طباعة تقرير الفحص المعملي"), function () {
//                 window.open("/printview?doctype=Lab%20Sample&name=" + frm.doc.name + "&trigger_print=1&format=%D8%AA%D9%82%D8%B1%D9%8A%D8%B1%20%D9%81%D8%AD%D8%B5%20%D9%85%D8%B9%D9%85%D9%84%D9%8A&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar")
//             });
//         }
//     },
//     refresh: function (frm) {
//         if (!frm.is_new()) { 
//             frm.add_custom_button(__("طباعة تقرير الفحص المعملي"), function () {
//                 window.open("/printview?doctype=Lab%20Sample&name=" + frm.doc.name + "&trigger_print=1&format=%D8%AA%D9%82%D8%B1%D9%8A%D8%B1%20%D9%81%D8%AD%D8%B5%20%D9%85%D8%B9%D9%85%D9%84%D9%8A&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar")
//             });
//         }
//     }
// });


frappe.ui.form.on("lab sample", "print_esal_tasleem", function (frm) {
	var myWin = window.open(
    "/printview?doctype=Lab%20Sample&name=" +
    cur_frm.doc.name +
    "&trigger_print=1&format=%D8%A7%D8%B3%D8%AA%D9%84%D8%A7%D9%85%20%D9%86%D8%AA%D9%8A%D8%AC%D8%A9%20%D8%A7%D9%84%D8%AA%D8%AD%D9%84%D9%8A%D9%84&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar");
    frm.doc.workflow_state = "تم التسليم"    
    // frappe.call({
    //     method: "frappe.client.set_value",
    //     args: {
    //         doctype: "Sample",
    //         filters: { "name": frm.doc.sample_no },
    //         fieldname: "remaining_cost",
    //         value: 0.0
    //     },
    //     callback: function(response) {
    //         // Handle the response
    //     }
    // });
    


    // frappe.call({
    //     method: "frappe.client.set_value",
    //     args: {
    //         doctype: "Sample",
    //         filters: { "name": frm.doc.sample_no },
    //         fieldname: "remaining_cost",
    //         value: 0.0
    //     },
    //     callback: function(response) {
    //         // Handle the response
    //     }
    // });

    
	frappe.call({
		doc: frm.doc,
		method: "print_esal_tasleem_function",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
    
});


frappe.ui.form.on("lab sample", "print_lab_report", function (frm) {
	let is_printed = 0;
	$.each(cur_frm.doc.lab_print_logs || [], function (i, d) {
		if (cur_frm.doc.enable_print === 0 && d.esal_name == "تقرير فحص معملي" && d.print_number == cur_frm.doc.print_number ) {
			is_printed = 1;
		}
	})
	if (is_printed == 1) {
		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_number) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
	}
	if (is_printed == 0) {
	var myWin = window.open("/printview?doctype=Lab%20Sample&name=" + frm.doc.name + "&trigger_print=1&format=تقرير%20فحص%20معملي&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar");
	}
	cur_frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_lab_result_function",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
    
});




// frappe.ui.form.on('lab sample', {
//     refresh: function(frm) {
//         // Add a custom button for previewing the print format
//         frm.add_custom_button(__('معاينة طباعة التقرير'), function() {


//             // http://10.0.0.5/printview?doctype=Lab%20Sample&name=Lab-Res-68736&trigger_print=1&format=new%20taqrer&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en
//             // URL for the print format preview
//             var print_format_url = frappe.urllib.get_full_url(
//                 "/printview?doctype=Lab%20Sample&name=" + frm.doc.name + "&trigger_print=1&format=new%20taqrer&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar"
//             );

//             // Open the print format preview in a new tab
//             var previewWindow = window.open(print_format_url, '_blank');
//             // previewWindow.removeEventListener("mousemove", myFunction);


//             // previewWindow.onload = function() {
//             //     previewWindow.document.querySelector('.print-preview-sidebar').style.display = 'none !important';
//             //     previewWindow.document.querySelector('.page-head').style.display = 'none !important';
//             // };
//             // console.log(previewWindow)
//             // Inject CSS to hide print button in the new window
//             // previewWindow.onload = function() {
//             //     var style = previewWindow.document.createElement('style');
//             //     style.type = 'text/css';
//             //     style.media = 'print';
//             //     style.innerHTML = `
//             //         @media print {
//             //         .print-preview-sidebar {
//             //             display: none !important;
//             //         }
//             //     `;
//             //     previewWindow.document.head.appendChild(style);
//             // };
//         });
//     }
// });




// if (cur_frm.doc.mos_name && cur_frm.doc.card_no && cur_frm.doc.tsleem_dat) {
// frappe.ui.form.on("lab sample", {
//     validate: function (frm) {
//         if (!frm.is_new()) {
//             frm.add_custom_button(__("طباعة ايصال استلام"), function () {
//                 window.open(
//                     "/printview?doctype=Lab%20Sample&name=" +
//                     cur_frm.doc.name +
//                     "&trigger_print=1&format=%D8%A7%D8%B3%D8%AA%D9%84%D8%A7%D9%85%20%D9%86%D8%AA%D9%8A%D8%AC%D8%A9%20%D8%A7%D9%84%D8%AA%D8%AD%D9%84%D9%8A%D9%84&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar");
//             });
//         }
//         cur_frm.doc.workflow_state = "تم التسليم"
//     },
//     refresh: function (frm) {
//         if (!frm.is_new()) {
//             frm.add_custom_button(__("طباعة ايصال استلام"), function () {
//                 window.open(
//                     "/printview?doctype=Lab%20Sample&name=" +
//                     cur_frm.doc.name +
//                     "&trigger_print=1&format=%D8%A7%D8%B3%D8%AA%D9%84%D8%A7%D9%85%20%D9%86%D8%AA%D9%8A%D8%AC%D8%A9%20%D8%A7%D9%84%D8%AA%D8%AD%D9%84%D9%8A%D9%84&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar");
//             });
//         }
//         cur_frm.doc.workflow_state = "تم التسليم"

//     }
    
// });
// }

let tableStateStack = [];
let isMouseDown = false;
let startCell = null;

function addEventListenerToButton() {
    document.getElementById("add-row-button").addEventListener("click", addRow);
    document.getElementById("add-col-button").addEventListener("click", addColumn);
    document.getElementById("remove-row-button").addEventListener("click", removeRow);
    document .getElementById("remove-col-button").addEventListener("click", removeColumn);
    document.getElementById("merge-cells-button").addEventListener("click", mergeCells);
    document.getElementById("save-form-button").addEventListener("click", saveForm); // Add event listener for save button    
    document.getElementById("undo-button").addEventListener("click", undoAction);
    document.getElementById("italic-button").addEventListener("click", makeItalic);
    document.getElementById("bold-button").addEventListener("click", makeBold);
    document.getElementById("underline-button").addEventListener("click", makeunderline);
    document.getElementById("orederList-button").addEventListener("click", makeorederList);
    document.getElementById("unorederList-button").addEventListener("click", makeunorederList);
    document.getElementById("justifyLeft-button").addEventListener("click", makejustifyLeft);
    document.getElementById("justifyCenter-button").addEventListener("click", makejustifyCenter);
    document.getElementById("justifyRight-button").addEventListener("click", makejustifyRight);
    document.getElementById("clear-table-button").addEventListener("click", clearTable); // Add event listener for clear table button
}

function saveTableState() {
    let tableHTML = document.getElementById("dynamic-table-container").outerHTML;
    tableStateStack.push(tableHTML);
}

function undoAction() {
    if (tableStateStack.length > 0) {
        let lastState = tableStateStack.pop();
        document.getElementById("dynamic-table-container").innerHTML = lastState;
        reattachEventListeners();
    }
}

function clearTable() {
    saveTableState(); // Save state before making changes
    let table = document.getElementById("dynamic-table");
    while (table.rows.length > 0) {
        table.deleteRow(0);
    }
}

frappe.ui.form.on("lab sample", {
    refresh: function (frm) {
        if (!frm.sample_report_initialized) {
            injectDynamicTable(frm);
            $("#dynamic-table-container").html(frm.doc.table_html);
            reattachEventListeners();
        }
    },
    before_save: function (frm) {
        var table_html = $("#dynamic-table-container").html();
        convertTableNumbersToArabic();
        frm.set_value("table_html", table_html);
    },
});

function injectDynamicTable(frm) {
    let wrapper = frm.fields_dict.sample_report.$wrapper;
    let tableHTML = `
        <div id="dynamic-table-container">
            <div class="table-data">
                <table id="dynamic-table" class="custom-table" border="1">
    `;
    const numRows = 5;
    const numCols = 5;

    for (let i = 0; i < numRows; i++) {
        tableHTML += "<tr>";
        for (let j = 0; j < numCols; j++) {
            tableHTML += `<td contenteditable="true" dir="rtl" style="text-align: center;"></td>`;
        }
        tableHTML += "</tr>";
    }

    tableHTML += `
                    </table>
                </div>
                <br>
                <div class="btns">
                    <button type="button" class="custom-btn" id="undo-button" title="Undo" style="background: #e37300;border-color: #e37300;">تراجع </button>
                    <button type="button" class="custom-btn" id="add-row-button" title="Add Row">إضافة صف </button>
                    <button type="button" class="custom-btn" id="add-col-button" title="Add Column">إضافة عمود </button>
                    <button type="button" class="custom-btn" id="remove-row-button" title="Remove Row" style="background: #bd1717;border-color: #bd1717;">حذف صف </button>
                    <button type="button" class="custom-btn" id="remove-col-button" title="Remove Column" style="background: #bd1717;border-color: #bd1717;">حذف عمود </button>
                    <button type="button" class="custom-btn" id="merge-cells-button" title="Merge Cells" style="background: #842dc9;border-color: #842dc9;">دمج الخلايا </button>
                    <button type="button" class="custom-btn" id="italic-button" title="Italic" style="font-style: italic;">النص مائل</button>
                    <button type="button" class="custom-btn" id="bold-button" title="Bold">النص عريض</button>
                    <button type="button" class="custom-btn" id="underline-button" title="Underline" style="text-decoration: underline;">خط أسفل النص </button>
                    <button type="button" class="custom-btn" id="orederList-button" title="Ordered List"><ol style="padding: 0;margin: 0;direction: rtl;"><li>قائمة منسدلة </li></ol> </button>
                    <button type="button" class="custom-btn" id="unorederList-button" title="Unordered List"><ul style="padding: 0;margin: 0;direction: rtl;"><li>قائمة منسدلة </li></ul> </button>
                    <button type="button" class="custom-btn" id="justifyLeft-button" title="Justify Left" style="text-align: left">النص لليسار</button>
                    <button type="button" class="custom-btn" id="justifyCenter-button" title="Justify Center" style="text-align: center">النص في المنتصف</button>
                    <button type="button" class="custom-btn" id="justifyRight-button" title="Justify Right" style="text-align: right">النص لليمين</button>
                    <button type="button" class="custom-btn" id="clear-table-button" title="Clear Table" style="background: #000000;border-color: #000000;">حذف الجدول</button>
                    <button type="button" class="custom-btn" id="save-form-button" title="Save">حفظ</button>
                </div>
        </div>
    `;

    wrapper.html(tableHTML);
    convertTableNumbersToArabic();
    reattachEventListeners();
    saveTableState(); // Save initial state
}

function reattachEventListeners() {
    addEventListenerToButton();

    let table = document.getElementById("dynamic-table");
    for (let row of table.rows) {
        for (let cell of row.cells) {
            cell.addEventListener("click", handleCellClick);
            cell.contentEditable = true;
            cell.addEventListener("mouseup", handleMouseUp);
            cell.addEventListener("mousedown", handleMouseDown);
            cell.addEventListener("mouseover", handleMouseOver);
        }
    }
    convertTableNumbersToArabic();
}
function makeItalic() {
    saveTableState(); // Save state before making changes
    document.execCommand("italic");
}

function makeBold() {
    saveTableState(); // Save state before making changes
    document.execCommand("bold");
}
function makeunderline() {
    saveTableState(); // Save state before making changes
    document.execCommand("underline");
}
function makeorederList() {
    saveTableState(); // Save state before making changes
    document.execCommand("insertOrderedList");
}
function makeunorederList() {
    saveTableState(); // Save state before making changes
    document.execCommand("insertUnorderedList");
}
function makejustifyLeft() {
    saveTableState(); // Save state before making changes
    document.execCommand("justifyLeft");
}
function makejustifyCenter() {
    saveTableState(); // Save state before making changes
    document.execCommand("justifyCenter");
}
function makejustifyRight() {
    saveTableState(); // Save state before making changes
    document.execCommand("justifyRight");
}
function saveForm() {
    convertTableNumbersToArabic();
    cur_frm.save();
}
function handleCellClick(event) {
    saveTableState(); // Save state before making changes
    let target = event.target;
    if (target.tagName === "TD") {
        if (event.shiftKey) {
            target.classList.toggle("selected-cell");
        } else {
            clearSelection();
            target.classList.add("selected-cell");
        }
        event.stopPropagation();
    }
}

function clearSelection() {
    document.querySelectorAll("#dynamic-table .selected-cell").forEach((cell) => {
        cell.classList.remove("selected-cell");
    });
}
function addRow() {
    saveTableState(); // Save state before making changes
    let table = document.getElementById("dynamic-table");
    let row = table.insertRow(-1);
    for (let i = 0; i < table.rows[0].cells.length; i++) {
        let cell = row.insertCell(i);
        cell.contentEditable = true;
        cell.innerHTML = "";
        cell.dir = "rtl";
        cell.style.textAlign = "center";
        cell.addEventListener("click", handleCellClick);
        cell.addEventListener("mouseup", handleMouseUp);
        cell.addEventListener("mousedown", handleMouseDown);
        cell.addEventListener("mouseover", handleMouseOver);
    }
}
function addColumn() {
    saveTableState(); // Save state before making changes
    let table = document.getElementById("dynamic-table");
    for (let row of table.rows) {
        let cell = row.insertCell(-1);
        cell.contentEditable = true;
        cell.innerHTML = "";
        cell.dir = "rtl";
        cell.style.textAlign = "center";
        cell.addEventListener("click", handleCellClick);
        cell.addEventListener("mouseup", handleMouseUp);
        cell.addEventListener("mousedown", handleMouseDown);
        cell.addEventListener("mouseover", handleMouseOver);
    }
}
function removeRow() {
    saveTableState(); // Save state before making changes
    let table = document.getElementById("dynamic-table");
    let selectedCells = getSelectedCells(table);

    if (selectedCells.length > 0) {
        let rowIndex = selectedCells[0].parentNode.rowIndex;
        table.deleteRow(rowIndex);
    } else {
        frappe.msgprint("برجاء إختيار أى خلية في الصف المراد حذفه");
    }
}
function removeColumn() {
    saveTableState(); // Save state before making changes
    let table = document.getElementById("dynamic-table");
    let selectedCells = getSelectedCells(table);

    if (selectedCells.length > 0) {
        let cellIndex = selectedCells[0].cellIndex;
        for (let row of table.rows) {
            row.deleteCell(cellIndex);
        }
    } else {
        frappe.msgprint("برجاء إختيار أى خلية في العمود المراد حذفه");
    }
}
function mergeCells() {
    saveTableState(); // Save state before making changes
    let table = document.getElementById("dynamic-table");
    let selectedCells = getSelectedCells(table);

    if (selectedCells.length > 1) {
        let topLeftCell = selectedCells[0];
        let bottomRightCell = selectedCells[selectedCells.length - 1];
        let topLeftRowIndex = topLeftCell.parentNode.rowIndex;
        let topLeftCellIndex = topLeftCell.cellIndex;
        let bottomRightRowIndex = bottomRightCell.parentNode.rowIndex;
        let bottomRightCellIndex = bottomRightCell.cellIndex;

        mergeSelectedCells(
            table,
            topLeftRowIndex,
            topLeftCellIndex,
            bottomRightRowIndex,
            bottomRightCellIndex
        );
    } else {
        frappe.msgprint("برجاء إختيار أكثر من خلية للدمج");
    }
}
function getSelectedCells(table) {
    saveTableState(); // Save state before making changes
    let selectedCells = [];
    for (let row of table.rows) {
        for (let cell of row.cells) {
            if (cell.classList.contains("selected-cell")) {
                selectedCells.push(cell);
            }
        }
    }
    return selectedCells;
}
function mergeSelectedCells(table, startRow, startCol, endRow, endCol) {
    let newContent = "";
    for (let i = startRow; i <= endRow; i++) {
        for (let j = startCol; j <= endCol; j++) {
            let cell = table.rows[i].cells[j];
            newContent += cell.innerHTML + " ";
            if (i !== startRow || j !== startCol) {
                cell.style.display = "none";
            } else {
                cell.colSpan = endCol - startCol + 1;
                cell.rowSpan = endRow - startRow + 1;
                cell.innerHTML = newContent.trim();
            }
        }
    }
}
function handleMouseDown(event) {
    isMouseDown = true;
    startCell = event.target;
    startCell.classList.toggle("selected-cell");
}

function handleMouseOver(event) {
    if (isMouseDown) {
        let currentCell = event.target;
        clearSelection();
        selectCells(startCell, currentCell);
    }
}

function handleMouseUp() {
    isMouseDown = false;
    startCell = null;
}

function selectCells(start, end) {
    let table = document.getElementById("dynamic-table");
    let startRowIndex = start.parentNode.rowIndex;
    let startCellIndex = start.cellIndex;
    let endRowIndex = end.parentNode.rowIndex;
    let endCellIndex = end.cellIndex;

    for (
        let i = Math.min(startRowIndex, endRowIndex);
        i <= Math.max(startRowIndex, endRowIndex);
        i++
    ) {
        for (
            let j = Math.min(startCellIndex, endCellIndex);
            j <= Math.max(startCellIndex, endCellIndex);
            j++
        ) {
            table.rows[i].cells[j].classList.add("selected-cell");
        }
    }
}

function clearSelection() {
    document.querySelectorAll("#dynamic-table .selected-cell").forEach((cell) => {
        cell.classList.remove("selected-cell");
    });
}

function convertEnglishToArabicNumbers(input) {
    const englishToArabicMap = {
        0: "٠",
        1: "١",
        2: "٢",
        3: "٣",
        4: "٤",
        5: "٥",
        6: "٦",
        7: "٧",
        8: "٨",
        9: "٩",
    };

    return input
        .toString()
        .split("")
        .map((char) => {
            return englishToArabicMap[char] !== undefined
                ? englishToArabicMap[char]
                : char;
        })
        .join("");
}

function convertTableNumbersToArabic() {
    // Get the container with the table
    const container = document.getElementById("dynamic-table-container");
    // Use TreeWalker to traverse all text nodes
    const walker = document.createTreeWalker(
        container,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );

    // Replace English numbers with Arabic numbers in all text nodes
    let node;
    while ((node = walker.nextNode())) {
        node.nodeValue = convertEnglishToArabicNumbers(node.nodeValue);
    }
}

// CSS styles for better visuals
const style = document.createElement("style");
style.innerHTML = `
    .selected-cell {
        background-color: #f0f8ff;
    }
    #dynamic-table-container {
        margin-top: 15px;
        padding-left: 1rem;
    }
    .table-data{
        overflow-X: auto;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    #dynamic-table td {
        min-width: 100px;
        padding: 5px;
        text-align: center;
        font-size: 15px;
        font-weight: bold;
        color: black;
        cursor: pointer;
    }
    #dynamic-table button {
        margin: 5px;
    }
    .custom-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 121px;
        height: 34px;
        font-weight: bold;
        font-size: 12px;
        color: #fff;
        background-color: #2e5c8d;
        border: 1px solid #2e5c8d;
        border-radius: 0.25rem;
        transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        cursor: pointer;
    }

    .custom-btn:hover {
        color: #fff;
        background-color: #0056b3; /* Darken the background color on hover */
        border-color: #0056b3; /* Darken the border color on hover */
    }

    .custom-btn:focus {
        outline: 0;
        box-shadow: 0 0 0 0.2rem rgba(38, 143, 255, 0.5); /* Add a focus shadow */
    }

    .custom-btn:active {
        color: #fff;
        background-color: #004085; /* Darken the background color even more when active */
        border-color: #004085; /* Darken the border color even more when active */
    }

    .custom-btn.disabled, .custom-btn:disabled {
        opacity: 0.65;
    }    

    .custom-table {
        border-collapse: separate;
        border-spacing: 0;
    }
    .custom-table thead th {
        background-color: #000;
        color: #fff;
        font-weight: bold;
        text-align: center;
        border: 1px solid #000;
    }
    .custom-table tbody tr:nth-child(odd) {
        background-color: #fff;
    }
    .custom-table tbody tr:nth-child(even) {
        background-color: #fff;
    }
    .custom-table th, .custom-table td {
        padding: 15px;
        text-align: left;
        border: 1px solid #000
        
    }
    .custom-table th {
        font-weight: bold;
    }
    .custom-table tbody td:hover {
        background-color: #f4f5f6;
        color: #000
        font-weight: bold;
    }
    .custom-table tbody td:visited {
        background-color: #fff;
        color: #000
        font-weight: bold;
    }
    #save-form-button{
        background: #2c792f !important;
        border: 1px solid #2c792f !important;
    }
    .selected-cell {
        background-color: #c1d8ef !important
    }
    .btns{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
    }
    .btns button{
        margin: 5px;
        padding: 7px 10px;
    }

`;
document.head.appendChild(style);






// frappe.ui.form.on("lab sample", {
//     sample_no: function(frm) {
//         frm.set_query("sample_no", function() {
//             return {
//                 filters: {
//                     workflow_state: ["not in", ["تم التسليم", "تحت التسليم"]]
//                 }
//             };
//         });
//     }
// });




// 70560 --> عدس مايو 4 82
// 70561 --> مكرونه مايو 4 83
// 70562 --> رز مايو 4 84
// 70563 --> كمون مايو 4 85
// 70564 --> جبنه بيضاء مايو 4 86
// 70565 --> طقم ابيض نص كم ضباط مايو 4 274
// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

// frappe.ui.form.on('lab sample', {
//     refresh:function(frm){
//         frm.set_df_property("bon_settings", "cannot_delete_rows", true);
//         frm.set_df_property("bon_settings", "cannot_add_rows", true);
// 		frm.set_df_property("footer_settings", "cannot_delete_rows", true);
//         frm.set_df_property("footer_settings", "cannot_add_rows", true);
//     }
// });


frappe.ui.form.on('lab sample', {
    refresh: async function(frm) {
        if (!frm.doc.__islocal) {
            console.log(frm.fields_dict);
            $(frm.fields_dict.html_preview.wrapper).empty();

            try {
                // Fetch additional data on the server side
                const response = await frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Sample",
                        fieldname: ["entity_name", "sample_receipt_date" , "sample_no1"],
                        filters: { name: frm.doc.sample_no }
                    }
                });

                const additional_data = response.message;

                // Prepare context for rendering template
                const context = {
                    doc: frm.doc,
                    entity_name: additional_data.entity_name,
                    sample_receipt_date: additional_data.sample_receipt_date,
                    print_number: frm.doc.print_number,
                    sample_no: frm.doc.sample_no,
                    smaple_name: frm.doc.smaple_name,
                    sample_no1 : additional_data.sample_no1,
                    comming_sample_lab: frm.doc.comming_sample_lab,
                };

                console.log(context);

                // Render the template with context
                const template = frappe.render_template("lab_sample", context);
                $(frm.fields_dict["html_preview"].wrapper).html(template);
            } catch (error) {
                console.error("Error fetching data or rendering template:", error);
            }
        }
    }
});



// frappe.ui.form.on('lab sample', {
// 	validate: function(frm) {
//         console.log(frm.doc.scan_image)
//         if (frm.doc.scan_image) {
//             console.log(frm.doc.scan_image)
//             // $(frm.fields_dict.html_preview.wrapper).find("#cheque_preview").css('background-image','url(' + frm.doc.scan_image + ')');
//             frm.refresh()
//         }
		
// 	}
// });

