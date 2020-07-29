from frappe import _


def get_data():
    return {
        'fieldname': 'tenant',
        'non_standard_fieldnames': {
            'Sales Invoice': 'pm_tenant'
        },
        'transactions': [
            {
                'label': _('Documents'),
                'items': ['Property Maintenance', 'Tenant Violation', 'Rental Contract', 'Sales Invoice'],
            }
        ]
    }
