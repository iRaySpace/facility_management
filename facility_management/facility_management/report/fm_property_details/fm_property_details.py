# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import nowdate


def execute(filters=None):
    columns, data = _get_columns(filters), _get_data(filters)
    return columns, data


def _get_columns(filters):
    def make_column(label, fieldname, width, fieldtype="Data", options=""):
        return {
            "label": _(label),
            "fieldname": fieldname,
            "width": width,
            "fieldtype": fieldtype,
            "options": options,
        }

    return [
        make_column("Property", "name", 150, "Link", "Property"),
        make_column("Name of the Property", "property_name", 180),
        make_column("Property Number", "property_no", 180),
        make_column("Property Type", "property_type", 180),
        make_column("Property Address", "property_addr", 180),
        make_column("Status", "status", 130),
    ]


def _get_data(filters):
    properties = _get_properties()
    return properties


def _get_properties():
    return frappe.get_all(
        "Property",
        fields=[
            "name",
            "property_group as property_name",
            "property_no",
            "property_type",
            "property_floor as property_addr",
            "rental_status as status",
        ],
    )
