frappe.ui.form.on('Sales Invoice', {
  refresh: function(frm) {
    _create_unlink_btn(frm);
  },
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


function _create_unlink_btn(frm) {
  if (frm.doc.__islocal) {
    return;
  }
  frm.add_custom_button(__('Unlink from Contract'), function () {
    _unlink_from_contract(frm.doc.name, frm.doc.pm_rental_contract);
  });
}

async function _unlink_from_contract(invoice, rental_contract) {
  const { message: result } = await frappe.call({
    method: 'facility_management.api.sales_invoice.unlink_from_rental_contract',
    args: { invoice },
  });
  if (result) {
    frappe.msgprint(__("Unlinked successfully. You may now delete or cancel the document"));
  }
}
