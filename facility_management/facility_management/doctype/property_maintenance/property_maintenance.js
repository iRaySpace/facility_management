// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'facility_management/facility_management/doctype/property_maintenance/property_maintenance_dialog.js' %}

frappe.ui.form.on('Property Maintenance', {
	refresh: function(frm) {
        _set_custom_buttons(frm);
	}
});

function _set_custom_buttons(frm) {
    frm.add_custom_button(__('Close'), async function() {
        await frm.call('close_issue');
        frm.save();
    });
    frm.add_custom_button(__('Log'), async function() {
        const { status, description } = await prompt_log();
        await frm.call('log_history', { status, description });
        frm.save();
    });
}
