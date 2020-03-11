// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'facility_management/facility_management/doctype/tenant/js_controllers/index.js' %}

frappe.ui.form.on('Tenant', {
	refresh: refresh,
	tenant_type: tenant_type,
	first_name: first_name,
	last_name: last_name,
});
