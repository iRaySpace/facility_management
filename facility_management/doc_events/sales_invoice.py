import frappe
from toolz import first


def validate(doc, method):
    _set_missing_values(doc)
    _set_rental_contract_item(doc)


def _set_missing_values(invoice):
    if not invoice.customer_name:
        invoice.customer_name = frappe.get_value(
            "Customer", invoice.customer, "customer_name"
        )

    if invoice.pm_rental_contract:
        rental_contract = frappe.get_all(
            "Rental Contract",
            filters={"name": invoice.pm_rental_contract},
            fields=["tenant", "property", "property_group"],
        )[0]
        property_group = rental_contract.get("property_group")
        cost_center = frappe.get_value(
            "Real Estate Property", property_group, "cost_center"
        )

        invoice.pm_property_group = property_group
        invoice.pm_tenant = rental_contract.get("tenant")
        invoice.pm_property = rental_contract.get("property")

        if not invoice.remarks:
            invoice.remarks = invoice.pm_rental_contract

        for item in invoice.items:
            item.cost_center = cost_center


def _set_rental_contract_item(doc):
    rental_contract_items = frappe.get_all(
        "Rental Contract Item",
        filters={"parent": doc.pm_rental_contract, "invoice_date": doc.due_date},
    )
    if rental_contract_items:
        rental_contract_item = first(rental_contract_items)
        description = f"Rent {doc.status}"
        frappe.db.set_value(
            "Rental Contract Item",
            rental_contract_item.get("name"),
            "description",
            description,
        )
