from frappe import _


def get_data():
    return [
        {
            'label': _('Documents'),
            'items': [
                {
                    'type': 'doctype',
                    'name': 'Property'
                },
                {
                    'type': 'doctype',
                    'name': 'Property Checkup'
                },
                {
                    'type': 'doctype',
                    'name': 'Property Facility'
                },
                {
                    'type': 'doctype',
                    'name': 'Property History'
                },
                {
                    'type': 'doctype',
                    'name': 'Property Inventory'
                },
                {
                    'type': 'doctype',
                    'name': 'Property Maintenance'
                },
                {
                    'type': 'doctype',
                    'name': 'Property Rental Type'
                },
                {
                    'type': 'doctype',
                    'name': 'Real Estate Property'
                },
                {
                    'type': 'doctype',
                    'name': 'Tenant'
                },
                {
                    'type': 'doctype',
                    'name': 'Tenant Renting'
                }
            ]
        },
        {
            'label': _('Employees'),
            'items': [
                {
                    'type': 'doctype',
                    'name': 'Employee'
                },
                {
                    'type': 'doctype',
                    'name': 'Expense Claim'
                }
            ]
        },
        {
            'label': _('Setup'),
            'items': [
                {
                    'type': 'doctype',
                    'name': 'Facility Management Settings'
                }
            ]
        }
    ]
