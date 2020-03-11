# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now


class PropertyMaintenance(Document):
	def close_issue(self):
		self.status = 'Closed'
		self.append('items', {
			'activity_datetime': now(),
			'status': 'Closed',
		})
		_send_email(self, 'Closed', 'Check Issue')

	def log_history(self, status, description):
		self.status = status
		self.append('items', {
			'activity_datetime': now(),
			'status': status,
			'description': description,
		})
		_send_email(self, status, description)


def _send_email(property_maintenance, status, description):
	if not property_maintenance.email_notification:
		return
	if not property_maintenance.email:
		frappe.throw(_('Email is not set'))
	try:
		frappe.sendmail(
			recipients=[property_maintenance.email],
			subject=f'Issue {property_maintenance.name} on {status}',
			message=description
		)
	except:
		frappe.msgprint('Unable to send email')
