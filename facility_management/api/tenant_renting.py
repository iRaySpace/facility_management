from functools import reduce

import frappe
from frappe.utils.data import nowdate


@frappe.whitelist()
def get_rental_listing():
    def data_occupied(rental):
        name = rental.get("name")
        return {"occupied": name in rented_properties}

    rented_properties = _get_rented_properties()
    occupied = list(map(data_occupied, _get_rental_properties()))

    return {
        "Vacant": len(list(filter(lambda x: not x["occupied"], occupied))),
        "Occupied": len(list(filter(lambda x: x["occupied"], occupied))),
    }


@frappe.whitelist()
def get_customer(tenant_renting):
    """
    Deprecated
    :param tenant_renting:
    :return:
    """
    tenant = frappe.db.get_value("Rental Contract", tenant_renting, "tenant")
    return frappe.db.get_value("Tenant Master", tenant, "customer")


def get_landlord_details(property):
    landlord = frappe.db.get_value("Property", property, "landlord")
    cpr = frappe.db.get_value("Landlord", landlord, "cpr")
    return {"name": landlord, "cpr": cpr}


def get_tenant_details(tenant):
    tenant_details = frappe.db.sql(
        """
            SELECT tenant_name, cpr, passport_no
            FROM `tabTenant Master`
            WHERE name = %(tenant)s
        """,
        {"tenant": tenant},
        as_dict=1,
    )
    return tenant_details[0] if tenant_details else None


def _get_rental_properties():
    return frappe.db.sql(
        """
            SELECT
                p.name,
                p.title,
                p.property_type
            FROM `tabProperty` p
            WHERE p.property_status = 'Rental'
        """,
        as_dict=True,
    )


def _get_rented_properties():
    def make_data(tenant_renting):
        return tenant_renting.get("property")

    return list(
        map(
            make_data,
            frappe.db.sql(
                """
                    SELECT property 
                    FROM `tabTenant Renting`
                    WHERE %s BETWEEN contract_start_date AND contract_end_date
                """,
                nowdate(),
                as_dict=True,
            ),
        )
    )
