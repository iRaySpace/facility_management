import frappe
from functools import reduce


@frappe.whitelist()
def get():
    return {
        'labels': _get_labels(),
        'datasets': _get_datasets(),
    }


def _get_labels():
    return _get_rental_status_options()


def _get_datasets():
    def make_data(data, property):
        rental_status = property.get('rental_status')
        rental_data = data.get(rental_status, 0)
        data[rental_status] = rental_data + 1
        return data

    def make_values(data, options):
        values = []
        for option in options:
            values.append(data[option])
        return values

    properties = frappe.db.sql("""
        SELECT rental_status
        FROM `tabProperty`
        WHERE property_status = 'Rental'
    """, as_dict=1)

    return [
        {
            'values': make_values(
                reduce(make_data, properties, {}),
                _get_rental_status_options()
            )
        }
    ]


def _get_rental_status_options():
    docfield = frappe.get_all(
        'DocField',
        filters={'parent': 'Property', 'fieldname': 'rental_status'},
        fields=['options']
    )[0]
    options = docfield.get('options').split('\n')
    return list(filter(lambda x: x, options))
