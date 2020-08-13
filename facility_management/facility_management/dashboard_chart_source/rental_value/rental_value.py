import frappe
import json
from facility_management.utils.functools import sum_by, concat_not_empty


@frappe.whitelist()
def get(filters):
    filters = json.loads(filters)
    labels = _get_labels()
    datasets = _get_datasets(filters)
    return {
        'labels': labels,
        'datasets': datasets,
    }


def _get_labels():
    return ['Active', 'Possible']


def _get_datasets(filters):
    active_contracts = _get_active_contracts(filters)
    possible_contracts = _get_possible_contracts(filters)
    return [
        {
            'name': 'Actual vs Possible',
            'values': [
                sum_by('rental_amount', active_contracts),
                sum_by('rental_amount', possible_contracts)
            ]
        }
    ]


def _get_active_contracts(filters):
    print(_get_clauses(filters))
    rental_contracts = frappe.db.sql(
        """
            SELECT rc.rental_amount
            FROM `tabRental Contract` rc
            WHERE rc.docstatus = 1
            AND status = 'Active'
            {clauses}
        """.format(
            clauses=_get_clauses(filters) or ''
        ),
        filters,
        as_dict=1
    )
    return rental_contracts


def _get_possible_contracts(filters):
    rental_contracts = frappe.db.sql(
        """
            SELECT rc.rental_amount
            FROM `tabRental Contract` rc
            WHERE rc.docstatus = 1
            AND status != 'Active'
            {clauses}
        """.format(
            clauses=_get_clauses(filters) or ''
        ),
        filters,
        as_dict=1
    )
    return rental_contracts


def _get_clauses(filters):
    clauses = []
    if filters.get('property_group'):
        clauses.append('property_group = %(property_group)s')
    return concat_not_empty(' AND ', ' AND '.join(clauses))
