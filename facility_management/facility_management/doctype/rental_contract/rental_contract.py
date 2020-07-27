# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import add_to_date, getdate, nowdate
from facility_management.helpers import get_status


class RentalContract(Document):
	def autoname(self):
		posting_date = getdate(self.posting_date)
		last_name = frappe.db.get_value('Tenant Master', self.tenant, 'last_name')
		self.name = '-'.join([
			last_name,
			self.property,
			posting_date.strftime('%m'),
			posting_date.strftime('%y')
		])

	def validate(self):
		_validate_contract_dates(self)
		_validate_property(self)
		if not self.items:
			# _generate_advance_payment(self)
			_generate_items(self)
		_set_status(self)

	def on_submit(self):
		_set_property_as_rented(self)


def _set_status(renting):
	status = None

	if renting.docstatus == 0:
		status = 'Draft'
	elif renting.docstatus == 2:
		status = 'Cancelled'
	elif renting.docstatus == 1:
		status = get_status({
			'Active': [
				renting.contract_end_date > nowdate()
			],
			'Expired': [
				renting.contract_end_date < nowdate()
			]
		})

	renting.db_set('status', status, update_modified=True)


def _validate_contract_dates(renting):
	if renting.contract_start_date > renting.contract_end_date:
		frappe.throw(_('Please set contract end date after the contract start date'))


def _validate_property(renting):
	rental_status = frappe.db.get_value('Property', renting.property, 'rental_status')
	if rental_status == 'Rented':
		frappe.throw(_('Please make choose unoccupied property.'))


def _generate_advance_payment(renting):
	"""
		Create items for advance payment
		:param renting:
		:return:
		"""
	renting.append('items', {
		'invoice_date': renting.posting_date,
		'description': 'Advance Payment',
		'is_invoice_created': 0
	})


def _generate_items(renting):
	"""
	Create items for succeeding dates
	:param renting:
	:return:
	"""
	end_date = getdate(renting.contract_end_date)
	next_date = _get_next_date(getdate(renting.start_invoice_date), renting.rental_frequency)
	while next_date < end_date:
		renting.append('items', {
			'invoice_date': next_date,
			'description': 'Rent Due',
			'is_invoice_created': 0
		})
		next_date = _get_next_date(next_date, renting.rental_frequency)


def _set_property_as_rented(renting):
	frappe.db.set_value('Property', renting.property, 'rental_status', 'Rented')


def _get_next_date(date, frequency):
	next_date = date
	if frequency == 'Monthly':
		next_date = add_to_date(next_date, months=1)
	elif frequency == 'Quarterly':
		next_date = add_to_date(next_date, months=4)
	elif frequency == 'Half-yearly':
		next_date = add_to_date(next_date, months=6)
	elif frequency == 'Yearly':
		next_date = add_to_date(next_date, years=1)
	return next_date
