frappe.provide('frappe.dashboards.chart_sources');


frappe.dashboards.chart_sources['Rental Property Occupancy'] = {
    method: 'facility_management.facility_management.dashboard_chart_source.rental_property_occupancy.rental_property_occupancy.get'
}
