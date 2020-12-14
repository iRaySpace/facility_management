# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.rename_doc import rename_doc
from erpnext.accounts.party import get_dashboard_info


class TenantMaster(Document):
	def onload(self):
		info = get_dashboard_info('Customer', self.customer)
		self.set_onload('dashboard_info', info)

	def autoname(self):
		if frappe.db.get_single_value("Facility Management Settings", "tenant_naming_by") == "Tenant Name":
			self.name = self.tenant_name

	def after_rename(self, old, new, merge):
		if self.customer:
			rename_doc('Customer', self.customer, new)

	def validate(self):
		_validate_tenant_name(self)

	def after_insert(self):
		_create_customer(self)


def _validate_tenant_name(tenant):
	if tenant.tenant_type == 'Company':
		tenant.first_name = ''
		tenant.last_name = ''
	else:
		if not tenant.first_name or not tenant.last_name:
			frappe.throw(_('Please input first and last names for the Individual'))
		tenant.tenant_name = ' '.join([tenant.first_name, tenant.last_name])


def _create_customer(tenant):
	customer_group = frappe.get_value('Selling Settings', None, 'customer_group')
	territory = frappe.get_value('Selling Settings', None, 'territory')
	if not (customer_group and territory):
		frappe.throw(_('Please set default customer group and territory in Selling Settings'))

	customer = frappe.get_doc({
		'doctype': 'Customer',
		'customer_name': tenant.tenant_name,
		'customer_group': customer_group,
		'territory': territory,
		'customer_type': 'Individual'
	})
	customer.insert(ignore_permissions=True)

	frappe.db.set_value('Tenant Master', tenant.name, 'customer', customer.name)
	frappe.msgprint(_('Customer {0} is created').format(customer.name), alert=True)
