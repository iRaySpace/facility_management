import frappe


def validate(doc, method):
    _set_missing_values(doc)


def _set_missing_values(invoice):
    if not invoice.customer_name:
        invoice.customer_name = frappe.get_value('Customer', invoice.customer, 'customer_name')

    if invoice.pm_rental_contract:
        rental_contract = frappe.get_all(
            'Rental Contract',
            filters={'name': invoice.pm_rental_contract},
            fields=['tenant', 'property', 'property_group']
        )[0]
        property_group = rental_contract.get('property_group')
        cost_center = frappe.get_value('Real Estate Property', property_group, 'cost_center')

        invoice.pm_property_group = property_group
        invoice.pm_tenant = rental_contract.get('tenant')
        invoice.pm_property = rental_contract.get('property')
        invoice.remarks = invoice.pm_rental_contract

        for item in invoice.items:
            item.cost_center = cost_center
