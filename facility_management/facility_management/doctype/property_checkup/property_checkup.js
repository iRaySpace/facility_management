// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'facility_management/facility_management/doctype/property_checkup/property_checkup_data.js' %}

frappe.ui.form.on('Property Checkup', {
	refresh: function(frm) {

	},
	property: async function(frm) {
	    _fetch_items(frm);
	}
});

async function _fetch_items(frm) {
    const property = frm.doc.property;
    const items = await get_items(property);
    items.forEach((item) => {
        const child = frm.add_child('items');
        frappe.model.set_value(child.doctype, child.name, 'item', item.item);
    });
    frm.refresh_field('items');
}
