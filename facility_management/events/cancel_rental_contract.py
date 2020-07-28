import frappe
from frappe.utils.data import today


def execute():
    rental_contracts = frappe.db.sql(
        """
            SELECT name
            FROM `tabRental Contract`
            WHERE docstatus = 1
            AND cancellation_date < %s
        """,
        today(),
        as_dict=1
    )
    for rental_contract in rental_contracts:
        rental_contract_doc = frappe.get_doc('Rental Contract', rental_contract['name'])
        rental_contract_doc.cancel()
