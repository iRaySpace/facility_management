import frappe


@frappe.whitelist()
def get_property_details(rental_contract):
    rental_contract_doc = frappe.get_all(
        'Rental Contract',
        filters={'name': rental_contract},
        fields=['tenant', 'property']
    )
    if rental_contract_doc:
        rental_contract_doc = rental_contract_doc[0]
        customer = frappe.get_value('Tenant Master', rental_contract_doc.get('tenant'), 'customer')
        property_group = frappe.get_value('Property', rental_contract_doc.get('property'), 'property_group')
        return {
            **rental_contract_doc,
            'customer': customer,
            'property_group': property_group
        }
    return None
