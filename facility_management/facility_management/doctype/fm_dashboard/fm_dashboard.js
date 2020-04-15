// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'facility_management/facility_management/doctype/fm_dashboard/fm_dashboard_data.js' %}


frappe.ui.form.on('FM Dashboard', {
	refresh: function(frm) {
		_make_rental_listing_graph('div[title="rental_listing_html"]');
		_make_outstanding_balances(frm);
	},
	real_estate_property: function(frm) {
		_make_outstanding_balances(frm);
	}
});


function _make_outstanding_balances(frm) {
	frm.call('make_outstanding_balances');
}


async function _make_rental_listing_graph(parent) {
	const rental_listing_data = await get_rental_listing();
	const data = {
		labels: Object.keys(rental_listing_data),
		datasets: [ { values: Object.values(rental_listing_data) } ],
	};
	new Chart(parent, {
		title: __('Rental Listing Graph'),
		data,
		type: 'percentage',
		height: 250,
		colors: ['#7cd6fd', '#743ee2'],
	});
}
