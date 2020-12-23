import frappe
import json


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = True

    name = frappe.form_dict.name
    if name:
        context.contract = frappe.get_doc("Rental Contract", name)
    else:
        context.contracts = _get_contracts()


def _get_contracts():
    return frappe.get_all(
        "Rental Contract",
        fields=["name", "status", "property", "posting_date"],
    )


def _get_contract(name):
    return frappe.get_value(
        "Rental Contract",
        name,
        [
            "name",
            "property",
            "status",
            "contract_start_date",
            "contract_end_date",
            "deposit_amount",
            "rental_frequency",
            "rental_amount",
            "ewa_limit",
        ],
        as_dict=1,
    )
