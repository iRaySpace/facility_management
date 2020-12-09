# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    return _get_columns(filters), _get_data(filters)


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
        make_column("Name of the Property", "property_group", 180, "Link", "Real Estate Property"),
        make_column("Property Type", "property_type", 130),
        make_column("Property Number", "property_no", 130),
        make_column("Tenant", "tenant", 280, "Link", "Tenant Master"),
        make_column("Address", "address", 250),
        make_column("Mobile", "mobile_no", 110),
        make_column("Mobile 2", "mobile_no_2", 110),
        make_column("Email", "email", 210),
        make_column("CPR/CR No", "cr_no", 180),
        make_column("Contract Period Start", "contract_start_date", 130, "Date"),
        make_column("Contract Period End", "contract_end_date", 130, "Date"),
        make_column("Security Amount", "security_amount", 130, "Currency"),
        make_column("EWA Limit", "ewa_limit", 130, "Currency"),
        make_column("Furnished", "furnished", 130, "Data")
    ]


def _get_clauses(filters):
    clauses = []
    if filters.get("property_name"):
        clauses.append("tr.property_group = %(property_name)s")
    if filters.get("property_type"):
        clauses.append("p.property_type = %(property_type)s")
    if filters.get("property_no"):
        clauses.append("p.property_no = %(property_no)s")
    if filters.get("tenant"):
        clauses.append("tr.tenant = %(tenant)s")
    if filters.get("furnished"):
        clauses.append("p.furnished = %(furnished)s")
    return "".join([" AND ", " AND ".join(clauses)]) if clauses else ""


def _get_data(filters):
    def make_data(renting):
        return {
            "property_group": renting.get("property_group"),
            "property_type": renting.get("property_type"),
            "property_no": renting.get("property_no"),
            "tenant": renting.get("tenant"),
            "address": renting.get("property_floor"),
            "mobile_no": renting.get("mobile_no"),
            "mobile_no_2": renting.get("mobile_no_2"),
            "email": renting.get("email"),
            "cr_no": renting.get("cr_no"),
            "contract_start_date": renting.get("contract_start_date"),
            "contract_end_date": renting.get("contract_end_date"),
            "security_amount": renting.get("deposit_amount"),
            "ewa_limit": renting.get("ewa_limit"),
            "furnished": renting.get("furnished")
        }

    tenant_rentings = frappe.db.sql(
        """
        SELECT 
            tr.property_group,
            p.property_type,
            p.property_no,
            tr.tenant,
            p.property_floor,
            t.mobile_no,
            t.mobile_no_2,
            t.email,
            t.cr_no,
            tr.contract_start_date,
            tr.contract_end_date,
            tr.deposit_amount,
            tr.ewa_limit,
            p.furnished
        FROM `tabRental Contract` tr
        LEFT JOIN `tabTenant Master` t ON tr.tenant = t.name
        LEFT JOIN `tabProperty` p ON tr.property = p.name
        WHERE tr.docstatus = 1
        {clauses}
        """.format(clauses=_get_clauses(filters)),
        filters,
        as_dict=True,
    )

    return list(map(make_data, tenant_rentings))


def _get_monthly_rental(amount, frequency):
    rental_amount = amount
    if frequency == "Daily":
        rental_amount = rental_amount * 30
    elif frequency == "Weekly":
        rental_amount = rental_amount * 4
    elif frequency == "Yearly":
        rental_amount = rental_amount / 12
    return rental_amount
