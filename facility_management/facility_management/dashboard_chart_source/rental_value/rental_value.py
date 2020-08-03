import frappe
from facility_management.utils.functools import sum_by


@frappe.whitelist()
def get():
    return {
        'labels': _get_labels(),
        'datasets': _get_datasets(),
    }


def _get_labels():
    return ['Active', 'Possible']


def _get_datasets():
    active_contracts = _get_active_contracts()
    possible_contracts = _get_possible_contracts()
    return [
        {
            'name': 'Actual vs Possible',
            'values': [
                sum_by('rental_amount', active_contracts),
                sum_by('rental_amount', possible_contracts)
            ]
        }
    ]


def _get_active_contracts():
    rental_contracts = frappe.db.sql("""
        SELECT rc.rental_amount
        FROM `tabRental Contract` rc
        WHERE rc.docstatus = 1
        AND status = 'Active'
    """, as_dict=1)
    return rental_contracts


def _get_possible_contracts():
    rental_contracts = frappe.db.sql("""
        SELECT rc.rental_amount
        FROM `tabRental Contract` rc
        WHERE rc.docstatus = 1
        AND status != 'Active'
    """, as_dict=1)
    return rental_contracts
