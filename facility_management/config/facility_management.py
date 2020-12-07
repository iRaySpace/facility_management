from frappe import _


def get_data():
    return [
        {
            "label": _("Documents"),
            "items": [
                {"type": "doctype", "name": "Property"},
                {"type": "doctype", "name": "Property Checkup"},
                {"type": "doctype", "name": "Real Estate Property"},
                {"type": "doctype", "name": "Tenant Master"},
                {"type": "doctype", "name": "Rental Contract"},
                {"type": "doctype", "name": "EWA Billing"},
                {"type": "doctype", "name": "Tenant Violation"},
                {"type": "doctype", "name": "FM Dashboard Balance"},
                {"type": "doctype", "name": "FM Dashboard"},
            ],
        },
        {
            "label": _("Employees"),
            "items": [
                {"type": "doctype", "name": "Employee"},
                {"type": "doctype", "name": "Expense Claim"},
            ],
        },
        {
            "label": _("Setup"),
            "items": [
                {"type": "doctype", "name": "Facility Management Settings"},
                {"type": "doctype", "name": "Property Facility"},
                {"type": "doctype", "name": "Property History"},
                {"type": "doctype", "name": "Property Inventory"},
                {"type": "doctype", "name": "Property Maintenance"},
            ],
        },
        {
            "label": _("Key Reports"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "FM Rental",
                    "onboard": 1,
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "FM Tenant",
                    "onboard": 1,
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "FM Property Details",
                    "onboard": 1,
                },
            ],
        },
    ]
