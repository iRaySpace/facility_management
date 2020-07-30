frappe.provide('frappe.dashboards.chart_sources');


frappe.dashboards.chart_sources['Rental Billing'] = {
    method: 'facility_management.facility_management.dashboard_chart_source.rental_billing.rental_billing.get'
}
