frappe.ui.form.on('Sales Invoice', {
  pm_tenant_renting: function(frm) {
    _set_customer(frm);
  }
});


async function _set_customer(frm) {
  frm.set_value('customer', await _get_customer(frm.doc.pm_tenant_renting));
}


async function _get_customer(tenant_renting) {
  const { message: customer } = await frappe.call({
    method: 'facility_management.api.tenant_renting.get_customer',
    args: { tenant_renting }
  });
  return customer;
}
