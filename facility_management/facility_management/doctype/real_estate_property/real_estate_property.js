// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Real Estate Property', {
  onload: function (frm) {
    frm.set_query('cost_center', function () {
      return {
        filters: { is_group: 0 },
      };
    });
  },
  refresh: function (frm) {
    _set_dashboard_indicators(frm);
  },
  insured: function (frm) {
    // TODO: commons
    const reqd_fields = [
      'insurance_company',
      'insurance_type',
      'insurance_start_date',
      'insurance_end_date',
    ];
    reqd_fields.forEach((reqd_field) =>
      frm.set_df_property(reqd_field, 'reqd', frm.doc.insured),
    );
  },
});

function _set_dashboard_indicators(frm) {
  if (frm.doc.__onload && frm.doc.__onload.dashboard_info) {
    const info = frm.doc.__onload.dashboard_info;
    frm.dashboard.add_indicator(
      __('Total Rented: {0}', [info.rented]),
      'orange',
    );
    frm.dashboard.add_indicator(
      __('Total Vacant: {0}', [info.vacant]),
      'orange',
    );
    frm.dashboard.add_indicator(
      __('Total Properties: {0}', [info.properties]),
      'blue',
    );
  }
}
