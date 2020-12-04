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
        make_column("Tenant", "tenant", 130, "Link", "Tenant Master"),
        make_column("Property Occupied", "property_occupied", 180, "Link", "Property"),
        make_column("Lease Start Date", "lease_start_date", 130, "Date"),
        make_column("Lease End Date", "lease_end_date", 130, "Date"),
        make_column("Monthly Rental", "monthly_rental", 110, "Currency"),
        make_column("Unpaid Amount", "unpaid_amount", 110, "Currency"),
        make_column("Employer", "employer_name", 130),
        make_column("Mobile", "mobile_no", 90),
        make_column("Mobile 2", "mobile_no_2", 90),
        make_column("Email", "email", 110),
    ]


def _get_data(filters):
    def make_data(renting):
        rental_amount = renting.get("rental_amount")
        rental_frequency = renting.get("rental_frequency")
        monthly_rental = _get_monthly_rental(rental_amount, rental_frequency)
        return {
            "tenant": renting.get("tenant"),
            "property_occupied": renting.get("property"),
            "lease_start_date": renting.get("contract_start_date"),
            "lease_end_date": renting.get("contract_end_date"),
            "monthly_rental": monthly_rental,
            "unpaid_amount": 0.00,
            "employer_name": renting.get("employer_name"),
            "mobile_no": renting.get("mobile_no"),
            "mobile_no_2": renting.get("mobile_no_2"),
            "email": renting.get("email"),
        }

    tenant_rentings = frappe.db.sql(
        """
        SELECT 
            tr.tenant,
            tr.property,
            tr.contract_start_date,
            tr.contract_end_date,
            tr.rental_frequency,
            tr.rental_amount,
            t.employer_name,
            t.mobile_no,
            t.mobile_no_2,
            t.email
        FROM `tabRental Contract` tr
        LEFT JOIN `tabTenant Master` t ON tr.tenant =  t.name
        """,
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
