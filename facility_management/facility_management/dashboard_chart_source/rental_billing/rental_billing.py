import frappe
import json
from frappe.utils.data import nowdate, add_months, getdate
from facility_management.utils.functools import group_by, sum_by, get_first_and_pluck_by, concat_not_empty
from functools import reduce

_month_range = 6


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
    return _get_months()


def _get_datasets(filters):
    def make_month_si(data):
        posting_date = data.pop('posting_date')
        data['month'] = posting_date.strftime('%b')
        data['paid_amount'] = data['grand_total'] - data['outstanding_amount']
        return data

    sales_invoices = frappe.db.sql(
        """
            SELECT
                grand_total,
                outstanding_amount,
                posting_date
            FROM `tabSales Invoice`
            WHERE docstatus = 1
            AND posting_date BETWEEN %(from_date)s AND %(to_date)s
            {clauses}
        """.format(
            clauses=_get_clauses(filters) or ''
        ),
        {
            **filters,
            'from_date': add_months(nowdate(), -_month_range),
            'to_date': nowdate()
        },
        as_dict=1
    )

    data = list(map(make_month_si, sales_invoices))
    grand_total = _get_total_by_month('grand_total', data)
    paid_total = _get_total_by_month('paid_amount', data)
    unpaid_total = _get_total_by_month('outstanding_amount', data)

    return [
        {
            'name': 'Total Billed Rent',
            'values': _get_values(grand_total)
        },
        {
            'name': 'Total Paid',
            'values': _get_values(paid_total)
        },
        {
            'name': 'Total Unpaid',
            'values': _get_values(unpaid_total)
        }
    ]


def _get_clauses(filters):
    clauses = []
    if filters.get('property_group'):
        clauses.append('pm_property_group = %(property_group)s')
    return concat_not_empty(' AND ', ' AND '.join(clauses))


def _get_months():
    def make_data(x):
        current_date = add_months(today, -x)
        return current_date.strftime('%b')
    today = getdate()
    months = list(map(make_data, range(_month_range)))
    return list(reversed(months))


def _get_total_by_month(key, data):
    def make_data(row):
        return {row: sum_by(key, grouped_data[row])}
    grouped_data = group_by('month', data)
    return list(map(make_data, grouped_data.keys()))


def _get_values(total_by_month):
    def make_data(total, month):
        total.append(get_first_and_pluck_by(month, total_by_month) or 0.00)
        return total
    months = _get_months()
    return reduce(make_data, months, [])
