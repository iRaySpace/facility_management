# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from toolz import pluck, merge


class RealEstateProperty(Document):
    def onload(self):
        property_status = _get_property_status(self.name)
        property_rent = _get_property_rent(self.name)
        self.set_onload("dashboard_info", merge(property_status, property_rent))

    def validate(self):
        _validate_abbr(self)


def _validate_abbr(property):
    if not property.abbr:
        property.abbr = "".join([c[0] for c in property.name.split()]).upper()

    property.abbr = property.abbr.strip()

    if not property.abbr:
        frappe.throw(_("Abbreviation is mandatory"))

    if frappe.get_all(
        "Real Estate Property",
        filters=[["abbr", "=", property.abbr], ["name", "!=", property.name]],
    ):
        frappe.throw(_("Abbreviation already used for another property"))


def _get_property_status(property_group):
    properties = list(
        pluck(
            "rental_status",
            frappe.db.sql(
                """
            SELECT rental_status 
            FROM `tabProperty` 
            WHERE property_group = %s
        """,
                property_group,
                as_dict=1,
            ),
        )
    )
    return {
        "rented": properties.count("Rented"),
        "vacant": properties.count("Vacant"),
        "properties": len(properties),
    }


# Total Paid, total Unpaid, total rent.
def _get_property_rent(property_group):
    sales_invoices = frappe.db.sql(
        """
            SELECT grand_total, outstanding_amount
            FROM `tabSales Invoice`
            WHERE pm_property_group = %s
            AND docstatus = 1
        """,
        property_group,
        as_dict=1,
    )

    grand_totals = sum(pluck("grand_total", sales_invoices))
    outstanding_amounts = sum(pluck("outstanding_amount", sales_invoices))

    return {
        "total_paid": grand_totals - outstanding_amounts,
        "total_unpaid": outstanding_amounts,
        "total_rent": grand_totals,
    }
