import frappe
from functools import reduce
from facility_management.utils.functools import group_by, sum_by, get_first_and_pluck_by


@frappe.whitelist()
def get():
    return {
        'labels': _get_labels(),
        'datasets': _get_datasets(),
    }


def _get_labels():
    return _get_property_types()


def _get_datasets():
    rental_contracts = _get_rental_contracts()
    total_by_property_type = _get_total_by_property_type(rental_contracts)
    return [
        {
            'name': 'Revenue per Month',
            'values': _get_values(total_by_property_type)
        }
    ]


def _get_property_types():
    docfield = frappe.get_all(
        'DocField',
        filters={'parent': 'Property', 'fieldname': 'property_type'},
        fields=['options']
    )[0]
    options = docfield.get('options').split('\n')
    return list(filter(lambda x: x, options))


def _get_rental_contracts():
    rental_contracts = frappe.db.sql("""
        SELECT rc.rental_amount, p.property_type
        FROM `tabRental Contract` rc
        INNER JOIN `tabProperty` p
        ON rc.property = p.name
        WHERE rc.docstatus = 1
        AND rc.status = 'Active'
    """, as_dict=1)
    return rental_contracts


def _get_total_by_property_type(rental_contracts):
    def make_data(row):
        return {row: sum_by('rental_amount', grouped_data[row])}
    grouped_data = group_by('property_type', rental_contracts)
    return list(map(make_data, grouped_data.keys()))


def _get_values(total_by_property_type):
    def make_data(total, property_type):
        total.append(get_first_and_pluck_by(property_type, total_by_property_type) or 0.00)
        return total
    property_types = _get_property_types()
    return reduce(make_data, property_types, [])
