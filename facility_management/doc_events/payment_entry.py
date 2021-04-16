import frappe
from frappe.utils.background_jobs import enqueue


def on_submit(doc, method):
    for ref in doc.references:
        if (
            ref.reference_doctype == "Sales Invoice"
            and ref.outstanding_amount == 0
        ):
            sales_invoice_doc = frappe.get_doc("Sales Invoice", ref.reference_name)
            enqueue(
                "facility_management.doc_events.sales_invoice.set_rental_contract_item",
                doc=sales_invoice_doc,
            )
