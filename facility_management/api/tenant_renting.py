from functools import reduce

import frappe
from frappe.utils.data import nowdate


@frappe.whitelist()
def get_rental_listing():
    def data_occupied(rental):
        name = rental.get('name')
        return {'occupied': name in rented_properties}

    rented_properties = _get_rented_properties()
    occupied = list(map(data_occupied, _get_rental_properties()))

    return {
        'Vacant': len(list(filter(lambda x: x['occupied'], occupied))),
        'Occupied': len(list(filter(lambda x: not x['occupied'], occupied)))
    }


@frappe.whitelist()
def get_customer(tenant_renting):
    tenant = frappe.db.get_value('Tenant Renting', tenant_renting, 'tenant')
    return frappe.db.get_value('Tenant', tenant, 'customer')


def _get_rental_properties():
    return frappe.db.sql("""
		SELECT
			p.name,
			p.title,
			p.property_type
		FROM `tabProperty` p
		WHERE p.property_status = 'Rental'
	""", as_dict=True)


def _get_rented_properties():
    def make_data(tenant_renting):
        return tenant_renting.get('property')

    return list(
        map(
            make_data,
            frappe.db.sql("""
				SELECT property 
				FROM `tabTenant Renting`
				WHERE %s 
				BETWEEN contract_start_date AND contract_end_date
			""", nowdate(), as_dict=True)
        )
    )
