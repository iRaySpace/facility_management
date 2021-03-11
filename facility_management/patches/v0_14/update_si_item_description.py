import frappe


def execute():
    data = frappe.db.get_all(
        "Sales Invoice Item",
        filters=[["description", "like", "Rent of %"]],
        fields=["name", "description"],
    )
    for row in data:
        description = row.get("description")
        new_description = description.replace("Rent of", "Rent (VAT Exempted) of")
        frappe.db.set_value("Sales Invoice Item", row.get("name"), "description", new_description)

