# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, enqueue
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils.data import add_to_date, getdate, nowdate, now_datetime, get_first_day
from facility_management.helpers import get_status
from facility_management.api.rental_contract import generate_invoices_now
from toolz import first


class RentalContract(Document):
    def autoname(self):
        abbr = frappe.db.get_value("Real Estate Property", self.property_group, "abbr")
        if not abbr:
            frappe.throw(
                _(
                    f"Please set the abbreviation of the Real Estate Property {self.property_group}"
                )
            )

        property_no = frappe.db.get_value("Property", self.property, "property_no")
        if not property_no:
            frappe.throw(
                _(f"Please set the property no of the Property {self.property}")
            )

        self.name = make_autoname("-".join([abbr, property_no, ".###"]), "", self)

    def validate(self):
        _validate_contract_dates(self)
        _validate_property(self)
        if not self.items or _updated_start_invoice_date(self):
            self.update({"items": _generate_items(self)})
        _set_status(self)
        _set_title(self)

    def on_submit(self):
        _set_property_as_rented(self)
        if self.apply_invoices_now:
            generate_invoices_now(self)

    def on_update_after_submit(self):
        _update_items(self)

    def before_cancel(self):
        _delink_sales_invoices(self)
        _set_property_as_vacant(self)
        _set_status(self)


def _set_status(renting):
    status = None

    if renting.docstatus == 0:
        status = "Draft"
    elif renting.docstatus == 2:
        status = "Cancelled"
    elif renting.docstatus == 1:
        status = get_status(
            {
                "Active": [renting.contract_end_date > nowdate()],
                "Expired": [renting.contract_end_date < nowdate()],
            }
        )

    renting.db_set("status", status, update_modified=True)


def _set_title(renting):
    if renting.is_new():
        renting.title = f"{renting.property} - {renting.tenant}"


def _validate_contract_dates(renting):
    if renting.contract_start_date > renting.contract_end_date:
        frappe.throw(_("Please set contract end date after the contract start date"))


def _validate_property(renting):
    rental_status = frappe.db.get_value("Property", renting.property, "rental_status")
    existing_rental_contracts = frappe.get_all(
        "Rental Contract", filters={"property": renting.property, "status": "Active"}
    )
    if existing_rental_contracts and rental_status == "Rented":
        existing_rental_contract = first(existing_rental_contracts)
        rental_contract_name = f'<strong>{existing_rental_contract.get("name")}</strong>'
        property_name = f'<strong>{renting.property}</strong>'
        frappe.throw(
            _(
                f"Property {property_name} is rented on Rental Contract {rental_contract_name}"
            )
        )


def _updated_start_invoice_date(renting):
    if not renting.items:
        return
    first_item = first(renting.items)
    if first_item.invoice_date != renting.start_invoice_date:
        return True


def _generate_items(renting):
    """
    Create items for succeeding dates
    :param renting:
    :return:
    """

    def make_item(invoice_date):
        return {
            "invoice_date": getdate(invoice_date),
            "description": "Rent Due",
            "is_invoice_created": 0,
        }

    items = []

    if _get_invoice_on_start_date():
        items.append(make_item(renting.start_invoice_date))

    end_date = getdate(renting.contract_end_date)
    next_date = _get_next_date(
        getdate(renting.start_invoice_date), renting.rental_frequency
    )
    while next_date < end_date:
        items.append(make_item(next_date))
        next_date = _get_next_date(next_date, renting.rental_frequency)

    return items


def _set_property_as_rented(renting):
    frappe.db.set_value("Property", renting.property, "rental_status", "Rented")


def _update_items(renting):
    existing_items = list(map(lambda x: x.invoice_date, renting.items))
    items = list(
        filter(
            lambda x: x.get("invoice_date").strftime("%Y-%m-%d") not in existing_items,
            _generate_items(renting),
        )
    )
    last_idx = len(existing_items)
    for count, item in enumerate(items):
        last_idx = last_idx + 1
        frappe.get_doc(
            {
                **item,
                "idx": last_idx,
                "doctype": "Rental Contract Item",
                "parent": renting.name,
                "parentfield": "items",
                "parenttype": "Rental Contract",
            }
        ).save()


def _delink_sales_invoices(renting):
    sales_invoices = frappe.get_all(
        "Sales Invoice", filters={"pm_rental_contract": renting.name}
    )
    for sales_invoice in sales_invoices:
        frappe.db.set_value("Sales Invoice", sales_invoice, "pm_rental_contract", "")


def _set_property_as_vacant(renting):
    retain_rental_on_cancel = frappe.db.get_single_value(
        "Facility Management Settings", "retain_rental_on_cancel"
    )
    if not retain_rental_on_cancel:
        frappe.db.set_value("Property", renting.property, "rental_status", "Vacant")


def _get_next_date(date, frequency):
    next_date = date
    if frequency == "Monthly":
        next_date = add_to_date(next_date, months=1)
    elif frequency == "Quarterly":
        next_date = add_to_date(next_date, months=4)
    elif frequency == "Half-yearly":
        next_date = add_to_date(next_date, months=6)
    elif frequency == "Yearly":
        next_date = add_to_date(next_date, years=1)
    return next_date


def _get_invoice_on_start_date():
    return frappe.db.get_single_value(
        "Facility Management Settings", "invoice_on_start_date"
    )
