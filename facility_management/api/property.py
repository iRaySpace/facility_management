import frappe
from frappe import _


def get_property_name(property):
    title, property_group = frappe.get_value(
        "Property", property, ["title", "property_group"]
    )

    address_line_1, city, country = frappe.get_value(
        "Real Estate Property", property_group, ["address_line_1", "city", "country"]
    )

    try:
        city_country = ", ".join([city, country])
        complete_address = " ".join([address_line_1, city_country])
    except:
        frappe.throw(_("Please set your Real Estate Property {}".format(property_group)))

    return ", ".join([title, complete_address])
