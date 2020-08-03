frappe.provide('frappe.dashboards.chart_sources');


frappe.dashboards.chart_sources['Rental Value'] = {
    method: 'facility_management.facility_management.dashboard_chart_source.rental_value.rental_value.get'
}
