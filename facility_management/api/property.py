import frappe


def get_property_name(property):
    title, property_group = frappe.get_value(
        "Property", property, ["title", "property_group"]
    )

    address_line_1, city, country = frappe.get_value(
        "Real Estate Property", property_group, ["address_line_1", "city", "country"]
    )
    city_country = ", ".join([city, country])
    complete_address = " ".join([address_line_1, city_country])

    return ", ".join([title, complete_address])
