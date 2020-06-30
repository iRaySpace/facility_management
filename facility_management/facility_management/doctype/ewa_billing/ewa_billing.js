// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('EWA Billing', {
	refresh: function(frm) {
	    _set_frm_props(frm);
	},
	set_posting_time: _set_posting_date_time,
});


frappe.ui.form.on('EWA Billing Item', {
    actual_ewa: function(frm, cdt, cdn) {
        const child = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'excess_amount', child.actual_ewa - child.incl_val);
    }
});


function _set_frm_props(frm) {
    _set_posting_date_time(frm);
    frm.set_df_property('company', 'hidden', 1);
}


function _set_posting_date_time(frm) {
    frm.set_df_property('posting_date', 'read_only', !frm.doc.set_posting_time);
    frm.set_df_property('posting_time', 'read_only', !frm.doc.set_posting_time);
}
