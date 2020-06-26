from frappe import _


def get_data():
    return {
        'fieldname': 'tenant',
        'transactions': [
            {
                'label': _('Documents'),
                'items': ['Property Maintenance', 'Tenant Violation'],
            }
        ]
    }
