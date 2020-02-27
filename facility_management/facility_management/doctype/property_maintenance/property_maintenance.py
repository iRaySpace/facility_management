# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import now


class PropertyMaintenance(Document):
	def close_issue(self):
		self.status = 'Closed'
		self.append('items', {
			'activity_datetime': now(),
			'status': 'Closed',
		})

	def log_history(self, status, description):
		self.status = status
		self.append('items', {
			'activity_datetime': now(),
			'status': status,
			'description': description,
		})

	def validate(self):
		if self.status == 'Closed':
			_send_email(self)


def _send_email(property_maintenance):
	email = frappe.get_value('Tenant', property_maintenance.tenant, 'email')
	try:
		frappe.sendmail(
			recipients=[email],
			subject=f'Issue {property_maintenance.name} has been closed',
			message=f'Description: {property_maintenance.issue_description}'
		)
	except:
		frappe.msgprint('Unable to send email')
