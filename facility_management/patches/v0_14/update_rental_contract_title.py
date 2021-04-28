import frappe


# bench execute facility_management.patches.v0_14.update_rental_contract_title.execute
def execute():
    data = frappe.get_all(
        "Rental Contract",
        fields=["name", "property", "tenant"]
    )
    for row in data:
        frappe.db.set_value(
            "Rental Contract",
            row.get("name"),
            "title",
            f"{row.get('property')} - {row.get('tenant')}"
        )
