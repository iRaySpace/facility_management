# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import nowdate


def execute(filters=None):
	columns, data = _get_columns(filters), _get_data(filters)
	return columns, data


def _get_columns(filters):
	def make_column(label, fieldname, width, fieldtype='Data', options=''):
		return {
			'label': _(label),
			'fieldname': fieldname,
			'width': width,
			'fieldtype': fieldtype,
			'options': options
		}

	return [
		make_column('Property Name', 'property_name', 130),
		make_column('Property', 'property', 180, 'Link', 'Property'),
		make_column('Property Type', 'property_type', 110),
		make_column('Is Occupied', 'is_occupied', 80, 'Check')
	]


def _get_data(filters):
	def make_data(rental):
		name = rental.get('name')
		return {
			'property': name,
			'property_name': rental.get('title'),
			'property_type': rental.get('property_type'),
			'is_occupied': name in rented_properties
		}
	rented_properties = _get_rented_properties()
	return list(map(make_data, _get_rental_properties()))


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
				FROM `tabRental Contract`
				WHERE %s
				BETWEEN contract_start_date AND contract_end_date
			""", nowdate(), as_dict=True)
		)
	)
