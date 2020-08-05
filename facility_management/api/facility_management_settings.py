import frappe


@frappe.whitelist()
def add_dashboard():
    dashboard = frappe.new_doc('Dashboard')
    dashboard.dashboard_name = 'Facility Management'
    for chart in ['Rental Value', 'Rental Revenue', 'Rental Billing', 'Rental Property Occupancy', 'Income', 'Expenses']:
        dashboard.append('charts', {'chart': chart})
    dashboard.save()
    return dashboard
