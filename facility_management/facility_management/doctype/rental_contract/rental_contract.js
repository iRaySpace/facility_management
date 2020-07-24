// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Contract', {
    onload: function(frm) {
        frm.set_query('property', function() {
            return {
                filters: {
                    rental_status: 'Vacant',
                }
            };
        });
    },
	refresh: function(frm) {
	    _add_payment_entry(frm);
	},
	contract_start_date: function(frm) {
	    _set_start_invoice_date(frm);
	}
});


function _add_payment_entry(frm) {
    if (frm.doc.docstatus !== 0) {
        frm.add_custom_button(__('Add Payment Entry'), async function() {
            const { message: tenant_master } = await frappe.db.get_value(
                'Tenant Master',
                frm.doc.tenant,
                'customer',
            );
            // ! hax ! (manually doing the route options of core and timing)
            frappe.__route_options = {
                mode_of_payment: 'Cash',
                party_type: 'Customer',
                party: tenant_master.customer,
                paid_amount: frm.doc.rental_amount,
            };
            frappe.new_doc('Payment Entry');
        });
    }
}


function _set_start_invoice_date(frm) {
    if (frm.doc.__islocal) {
        const start_invoice_date = frappe.datetime.add_days(frm.doc.contract_start_date, -7);
        frm.set_value('start_invoice_date', start_invoice_date);
    }
}
