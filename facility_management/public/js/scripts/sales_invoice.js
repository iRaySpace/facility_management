frappe.ui.form.on('Sales Invoice', {
  pm_rental_contract: function(frm) {
    _set_property_details(frm);
  }
});


async function _set_property_details(frm) {
  const property_details = await _get_property_details(frm.doc.pm_rental_contract);
  if (property_details) {
    frm.set_value('customer', property_details.customer);
    frm.set_value('pm_tenant', property_details.tenant);
    frm.set_value('pm_property', property_details.property);
    frm.set_value('pm_property_group', property_details.property_group);
  }
}


async function _get_property_details(rental_contract) {
  const { message: property_details } = await frappe.call({
    method: 'facility_management.api.sales_invoice.get_property_details',
    args: { rental_contract },
  });
  return property_details;
}
