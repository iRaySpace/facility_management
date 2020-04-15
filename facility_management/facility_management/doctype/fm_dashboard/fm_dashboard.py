# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class FMDashboard(Document):
	def make_outstanding_balances(self):
		"""
		Make outstanding balances for display
		:return:
		"""
		self.outstanding_balances = None

		outstanding_balances = _get_outstanding_balances(_get_properties(self.real_estate_property))
		for outstanding_balance in outstanding_balances:
			self.append('outstanding_balances', {
				'property_name': outstanding_balance.get('property_name'),
				'sales_invoice': outstanding_balance.get('sales_invoice'),
				'outstanding_amount': outstanding_balance.get('outstanding_amount')
			})


def _get_properties(real_estate_property):
	return list(map(lambda x: x['name'], frappe.get_all('Property', {'property_location': real_estate_property})))


def _get_outstanding_balances(filter_properties):
	def make_data(balance):
		property_name = _get_property_name(balance.get('pm_tenant_renting'))
		return {
			'property_name': property_name,
			'sales_invoice': balance.get('name'),
			'outstanding_amount': balance.get('outstanding_amount')
		}

	outstanding = frappe.db.sql("""
		SELECT 
			si.name, 
			si.pm_tenant_renting,
			si.outstanding_amount,
			tr.property
		FROM `tabSales Invoice` si
		LEFT JOIN `tabTenant Renting` tr ON si.pm_tenant_renting = tr.name
		WHERE si.docstatus = 1 
		AND si.outstanding_amount > 0
		AND si.pm_tenant_renting != ''
	""", as_dict=True)

	outstanding = filter(lambda x: x['property'] in filter_properties, outstanding)

	return list(map(make_data, outstanding))


def _get_property_name(tenant_renting):
	data = frappe.db.sql("""
		SELECT p.title
		FROM `tabTenant Renting` tr
		JOIN `tabProperty` p
		ON tr.property = p.name
		WHERE tr.name = %s
	""", tenant_renting, as_dict=True)
	return data[0]['title'] if data else None
