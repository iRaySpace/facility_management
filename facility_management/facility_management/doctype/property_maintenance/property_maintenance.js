// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'facility_management/facility_management/doctype/property_maintenance/property_maintenance_dialog.js' %}

frappe.ui.form.on('Property Maintenance', {
	refresh: function(frm) {
        _set_custom_buttons(frm);
	},
	tenant: function(frm) {
        _set_tenant_details(frm);
	}
});

function _set_custom_buttons(frm) {
    if (frm.doc.__islocal) {
        return;
    }
    frm.add_custom_button(__('Close'), async function() {
        await frm.call('close_issue');
        frm.savesubmit();
    });
    frm.add_custom_button(__('Log'), async function() {
        const { datetime, status, description } = await prompt_log();
        await frm.call('log_history', { datetime, status, description });
        frm.save();
    });

    // Add
    frm.add_custom_button(__('Expense Claim'), function() {
        frappe.route_options = {
            'pm_property_maintenance': frm.doc.name,
            'employee': frm.doc.assigned_to,
        };
        frappe.new_doc('Expense Claim');
    }, __('Add'));
    frm.add_custom_button(__('Material Request'), function() {
        frappe.route_options = {
            'pm_property_maintenance': frm.doc.name,
            'requested_by': frm.doc.assigned_to,
        };
        frappe.new_doc('Material Request');
    }, __('Add'));
    frm.add_custom_button(__('Asset Repair'), function() {
        frappe.route_options = {
            'pm_property_maintenance': frm.doc.name,
            'assign_to': frm.doc.created_by,
        };
        frappe.new_doc('Asset Repair');
    }, __('Add'));
}

async function _set_tenant_details(frm) {
    const tenant = await frappe.db.get_doc('Tenant Master', frm.doc.tenant);
    frm.set_value('tenant_name', `${tenant.first_name} ${tenant.last_name}`);
    frm.set_value('email', tenant.email);
}
