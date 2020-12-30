function refresh(frm) {
    frm.trigger('tenant_type');
    if (!frm.doc.__islocal) {
        erpnext.utils.set_party_dashboard_indicators(frm);
    } else {
      _setup_naming_series(frm);
    }
}

async function _setup_naming_series(frm) {
  const tenant_naming_by = await frappe.db.get_single_value("Facility Management Settings", "tenant_naming_by");
  if (tenant_naming_by !== "Naming Series") {
    frm.set_df_property("naming_series", "hidden", 1);
  }
}
