import json
import frappe
from frappe import _


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


@frappe.whitelist()
def get_statuses(invoices):
    invoices = json.loads(invoices)
    data = frappe.get_all(
        "Sales Invoice",
        fields=["name", "status"],
        filters=[["name", "in", invoices]]
    )
    return {x.get("name"): x.get("status") for x in data}


@frappe.whitelist()
def unlink_from_rental_contract(invoice):
    contract_items = frappe.get_all(
        "Rental Contract Item",
        filters={"invoice_ref": invoice}
    )
    if not contract_items:
        frappe.throw(_("There is no linked Rental Contract Item"))
    contract_item = contract_items[0]
    frappe.db.set_value("Rental Contract Item", contract_item.get("name"), "invoice_ref", "")
    frappe.db.set_value("Rental Contract Item", contract_item.get("name"), "is_invoice_created", 0)
    return True
