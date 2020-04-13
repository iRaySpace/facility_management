# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class Tenant(Document):
	def after_insert(self):
		_create_customer(self)


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

	frappe.db.set_value('Tenant', tenant.name, 'customer', customer.name)
	frappe.msgprint(_('Customer {0} is created').format(customer.name), alert=True)

