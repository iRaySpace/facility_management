# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from toolz import merge


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
        make_column(
            "Real Estate Property",
            "property_group",
            180,
            "Link",
            "Real Estate Property",
        ),
        make_column("Property Type", "property_type", 110),
        make_column("Property No", "property_no", 130),
        make_column("Floor Number", "property_floor", 250),
        make_column("Furnished", "furnished", 130, "Data"),
        make_column("Status", "rental_status", 130),
        make_column("Tenant Name", "tenant", 180, "Link", "Tenant Master"),
        make_column("Contact No", "mobile_no", 180),
        make_column("Contract Start Date", "contract_start_date", 180, "Date"),
        make_column("Contract End Date", "contract_end_date", 180, "Date"),
        make_column("Rental Amount", "rental_amount", 130, "Currency"),
        make_column("EWA Limit", "ewa_limit", 130, "Currency"),
        make_column("Security Amount", "deposit_amount", 130, "Currency"),
    ]


def _get_data(filters):
    properties = _get_properties()
    active_contracts = {x.get("property"): x for x in _get_active_contracts()}
    data = [merge(x, active_contracts.get(x.get("name"), {})) for x in properties]
    return data


def _get_properties():
    return frappe.get_all(
        "Property",
        fields=[
            "name",
            "property_group",
            "property_type",
            "property_no",
            "property_floor",
            "rental_status",
            "furnished",
        ],
    )


def _get_active_contracts():
    return frappe.db.sql(
        """
            SELECT
                rc.tenant,
                tm.mobile_no,
                rc.property,
                rc.contract_start_date,
                rc.contract_end_date,
                rc.deposit_amount,
                rc.rental_frequency,
                rc.rental_amount,
                rc.ewa_limit
            FROM `tabRental Contract` rc
            JOIN `tabTenant Master` tm ON rc.tenant = tm.name
            WHERE rc.status = 'Active'
        """,
        as_dict=1,
    )
