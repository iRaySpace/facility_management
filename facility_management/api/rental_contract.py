import frappe
from frappe import _
from frappe.utils.data import get_first_day, getdate, now_datetime
from facility_management.helpers import get_debit_to, set_invoice_created
from facility_management.utils.rental_contract import (
    make_description,
    make_item_description,
)


@frappe.whitelist()
def create_invoice(rental, rental_item):
    rental_contract = frappe.get_doc("Rental Contract", rental)
    rental_items = list(filter(lambda x: x.name == rental_item, rental_contract.items))
    _validate_rental_items(rental_items)
    generate_invoices_now(rental_contract, rental_items)
    return True


def _validate_rental_items(rental_items):
    rental_created = list(filter(lambda x: x.is_invoice_created, rental_items))
    if rental_created:
        frappe.throw(
            _(
                "Unable to generate an invoice. Rental Item has already invoice been generated."
            )
        )


def generate_invoices_now(renting, items=None):
    def make_data(item_data):
        return {
            "customer": customer,
            "due_date": item_data.invoice_date,
            "posting_date": get_first_day(item_data.invoice_date),
            "debit_to": debit_to,
            "set_posting_time": 1,
            "posting_time": 0,
            "pm_rental_contract": renting.name,
            "items": [
                {
                    "item_code": rental_item,
                    "description": make_item_description(
                        {
                            "property": renting.property,
                            "posting_date": item_data.invoice_date,
                        }
                    ),
                    "rate": renting.rental_amount,
                    "qty": 1,
                }
            ],
        }

    if not items:
        items = list(
            filter(
                lambda x: getdate(x.invoice_date) < getdate(now_datetime()),
                renting.items,
            )
        )

    customer = frappe.db.get_value("Tenant Master", renting.tenant, "customer")
    rental_item = frappe.db.get_single_value(
        "Facility Management Settings", "rental_item"
    )
    submit_si = frappe.db.get_single_value("Facility Management Settings", "submit_si")
    debit_to = get_debit_to()

    for item in items:
        invoice_data = make_data(item)
        items = invoice_data.pop("items")

        invoice = frappe.new_doc("Sales Invoice")
        invoice.update(invoice_data)
        invoice.append("items", items[0])
        invoice.set_missing_values()
        invoice.remarks = make_description(
            {
                "posting_date": invoice.posting_date,
                "property": renting.property,
                "rental_contract": renting.name,
            }
        )

        invoice.save()

        if submit_si:
            invoice.submit()

        set_invoice_created(item.name, invoice.name)
