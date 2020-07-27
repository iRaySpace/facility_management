from frappe import _


def get_data():
    return {
        'fieldname': 'property',
        'transactions': [
            {
                'label': _('Documents'),
                'items': ['Rental Contract'],
            }
        ]
    }
