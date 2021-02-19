import frappe


def execute():
    rental_contract_items = frappe.db.get_all(
        "Rental Contract Item",
        filters={"is_invoice_created": 1},
        fields=["name", "invoice_ref"],
    )
    for item in rental_contract_items:
        status = frappe.db.get_value("Sales Invoice", item.get("invoice_ref"), "status")
        frappe.db.set_value(
            "Rental Contract Item", item.get("name"), "description", f"Rent {status}"
        )
