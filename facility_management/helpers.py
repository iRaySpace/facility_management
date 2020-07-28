import frappe


def get_status(status_conditions):
    for key, values in status_conditions.items():
        if all(values):
            return key


def set_all_property_as_vacant():
    """
    bench execute facility_management.helpers.set_all_property_as_vacant
    :return:
    """
    properties = frappe.get_all('Property')
    for property_name in properties:
        frappe.db.set_value('Property', property_name, 'rental_status', 'Vacant')
