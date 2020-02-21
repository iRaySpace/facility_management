import frappe


@frappe.whitelist()
def get_items(property_name):
    return frappe.get_all(
        'Property Inventory',
        filters={'property': property_name},
        fields=['item']
    )
