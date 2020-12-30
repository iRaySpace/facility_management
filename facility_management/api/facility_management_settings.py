import frappe


@frappe.whitelist()
def add_dashboard():
    dashboard = frappe.new_doc('Dashboard')
    dashboard.dashboard_name = 'Facility Management'
    for chart in ['Rental Value', 'Rental Revenue', 'Rental Billing', 'Rental Property Occupancy', 'Income', 'Expenses']:
        dashboard.append('charts', {'chart': chart})
    dashboard.save()
    return dashboard


@frappe.whitelist()
def add_pages_to_portal():
    portal_settings = frappe.get_doc('Portal Settings', 'Portal Settings')
    menu = [
        {
            'title': 'Contracts',
            'enabled': True,
            'route': '/contracts',
            'reference_doctype': 'Rental Contract',
            'role': 'Customer',
        },
        {
            'title': 'Violations',
            'enabled': True,
            'route': '/violations',
            'reference_doctype': 'Tenant Violation',
            'role': 'Customer',
        },
        {
            'title': 'Maintenance List',
            'enabled': True,
            'route': '/maintenances',
            'reference_doctype': 'Property Maintenance',
            'role': 'Customer',
        },
        {
            'title': 'New Maintenance',
            'enabled': True,
            'route': '/new-maintenance',
            'reference_doctype': 'Property Maintenance',
            'role': 'Customer',
        },
        {
            'title': 'Receipts',
            'enabled': True,
            'route': '/receipts',
            'reference_doctype': 'Payment Entry',
            'role': 'Customer',
        },
        {
            'title': 'Personal Information',
            'enabled': True,
            'route': '/personal-information',
        },
    ]
    for row in menu:
        portal_settings.append('menu', row)
    portal_settings.save()
    return True
