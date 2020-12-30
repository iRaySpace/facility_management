// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Facility Management Settings', {
	refresh: function(frm) {
        _render_setup(frm);
	},
});


function _render_setup(frm) {
    frm.add_custom_button('Setup Dashboard', function() {
        frappe.call({ method: 'facility_management.api.facility_management_settings.add_dashboard' })
            .then(({ message }) => frappe.msgprint(__(`Dashboard ${message.name} has been created`)));
    });
    frm.add_custom_button('Setup Portal', async function() {
        const { message: response } = await frappe.call({
          method: 'facility_management.api.facility_management_settings.add_pages_to_portal'
        });
        if (response) {
          frappe.msgprint(__(`Added Pages to Portal`));
        }
    });
}
