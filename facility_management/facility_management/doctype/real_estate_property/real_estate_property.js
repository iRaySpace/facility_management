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
    _set_dashboard_charts(frm);
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
    frm.dashboard.add_indicator(__('Total Rented: {0}', [info.rented]), 'blue');
    frm.dashboard.add_indicator(
      __('Total Vacant: {0}', [info.vacant]),
      'orange',
    );
    frm.dashboard.add_indicator(
      __('Total Properties: {0}', [info.properties]),
      'green',
    );
    frm.dashboard.add_indicator(
      __('Expected Rent: {0}', [format_currency(info.total_expected_rent)]),
      'orange',
    );
    frm.dashboard.add_indicator(
      __('Total Paid: {0}', [format_currency(info.total_paid)]),
      'blue',
    );
    frm.dashboard.add_indicator(
      __('Total Unpaid: {0}', [format_currency(info.total_unpaid)]),
      'orange',
    );
    frm.dashboard.add_indicator(
      __('Total Rent: {0}', [format_currency(info.total_rent)]),
      'green',
    );
    frm.dashboard.add_indicator(
      __('Rent Actual: {0}', [format_currency(info.total_rent_actual)]),
      'orange',
    );
    $('.indicator-column').css('margin', '.25em 0');
  }
}

function _set_dashboard_charts(frm) {
  if (frm.doc.__onload && frm.doc.__onload.dashboard_info) {
    const info = frm.doc.__onload.dashboard_info;
    const data = {
      labels: ['Total Paid', 'Total Unpaid', 'Total Rent', 'Total Expected Rent', 'Total Rent Actual'],
      datasets: [
        { values: [info.total_paid, info.total_unpaid, info.total_rent, info.total_expected_rent, info.total_rent_actual] },
      ],
    };

    // from frm.dashboard.render_graph()
    frm.dashboard.chart_area.empty().removeClass('hidden');
    frm.dashboard.show();
    frm.dashboard.chart = new frappe.Chart('.form-graph', {
      type: 'bar',
      colors: ['green'],
      data: data,
    });
    if (!frm.dashboard.chart) {
      frm.dashboard.hide();
    }
  }
}
