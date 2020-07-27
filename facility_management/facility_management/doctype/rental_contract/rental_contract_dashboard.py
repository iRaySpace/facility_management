from frappe import _


def get_data():
    return {
        'fieldname': 'pm_rental_contract',
        'transactions': [
            {
                'label': _('Documents'),
                'items': ['Sales Invoice'],
            }
        ]
    }
