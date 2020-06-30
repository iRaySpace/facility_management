// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('EWA Billing', {
	refresh: function(frm) {
        _set_posting_date_time(frm);
	},
	set_posting_time: function(frm) {
	    _set_posting_date_time(frm);
	},
});


function _set_posting_date_time(frm) {
    frm.set_df_property('posting_date', 'read_only', !frm.doc.set_posting_time);
    frm.set_df_property('posting_time', 'read_only', !frm.doc.set_posting_time);
}
