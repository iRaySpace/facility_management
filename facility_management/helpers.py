import frappe


def get_status(status_conditions):
    for key, values in status_conditions.items():
        if all(values):
            return key


def get_debit_to():
    company = frappe.defaults.get_user_default('Company')
    return frappe.db.get_value('Company', company, 'default_receivable_account')


def set_invoice_created(name, invoice_ref):
    frappe.db.set_value('Rental Contract Item', name, 'is_invoice_created', 1)
    frappe.db.set_value('Rental Contract Item', name, 'invoice_ref', invoice_ref)


def set_all_property_as_vacant():
    """
    bench execute facility_management.helpers.set_all_property_as_vacant
    :return:
    """
    properties = frappe.get_all('Property')
    for property_name in properties:
        frappe.db.set_value('Property', property_name, 'rental_status', 'Vacant')
