// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Contract', {
	contract_start_date: function(frm) {
	    _set_start_invoice_date(frm);
	}
});

function _set_start_invoice_date(frm) {
    if (frm.doc.__islocal) {
        const start_invoice_date = frappe.datetime.add_months(frm.doc.contract_start_date, 1);
        frm.set_value('start_invoice_date', start_invoice_date);
    }
}
