import frappe


def execute():
    data = frappe.db.get_all(
        "Rental Contract",
        filters=[["docstatus", "=", 2], ["status", "=", "Active"]],
    )
    for row in data:
        frappe.db.set_value("Rental Contract", row.get("name"), "status", "Cancelled")
