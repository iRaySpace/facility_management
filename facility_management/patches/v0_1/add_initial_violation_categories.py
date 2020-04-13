import frappe


def execute():
    for violation_category in ['Building & Structure', 'Exteriors', 'General Rules', 'Noise', 'Pets', 'Trash',
                               'Vehicles & Parking', 'Others']:
        if not frappe.db.exists('Tenant Violation Category', violation_category):
            frappe.get_doc({
                'doctype': 'Tenant Violation Category',
                'category_name': violation_category
            }).insert()
