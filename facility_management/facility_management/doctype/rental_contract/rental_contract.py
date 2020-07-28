# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, enqueue
from frappe.model.document import Document
from frappe.utils.data import add_to_date, getdate, nowdate, now_datetime, get_first_day
from facility_management.helpers import get_status, get_debit_to, set_invoice_created


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
			_generate_items(self)
		_set_status(self)

	def on_submit(self):
		_set_property_as_rented(self)
		if self.apply_invoices_now:
			_generate_invoices_now(self)

	def before_cancel(self):
		_delink_sales_invoices(self)
		_set_property_as_vacant(self)


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


def _generate_items(renting):
	"""
	Create items for succeeding dates
	:param renting:
	:return:
	"""
	def make_item(invoice_date):
		return {
			'invoice_date': invoice_date,
			'description': 'Rent Due',
			'is_invoice_created': 0
		}

	if _get_invoice_on_start_date():
		renting.append('items', make_item(renting.start_invoice_date))

	end_date = getdate(renting.contract_end_date)
	next_date = _get_next_date(getdate(renting.start_invoice_date), renting.rental_frequency)
	while next_date < end_date:
		renting.append('items', make_item(next_date))
		next_date = _get_next_date(next_date, renting.rental_frequency)


def _set_property_as_rented(renting):
	frappe.db.set_value('Property', renting.property, 'rental_status', 'Rented')


def _generate_invoices_now(renting):
	def make_data(item_data):
		return {
			'customer': customer,
			'due_date': item_data.invoice_date,
			'posting_date': get_first_day(item_data.invoice_date),
			'debit_to': debit_to,
			'set_posting_time': 1,
			'posting_time': 0,
			'pm_rental_contract': renting.name,
			'items': [
				{
					'item_code': rental_item,
					'rate': renting.rental_amount,
					'qty': 1
				}
			]
		}

	items = list(filter(lambda x: getdate(x.invoice_date) < getdate(now_datetime()), renting.items))
	customer = frappe.db.get_value('Tenant Master', renting.tenant, 'customer')
	rental_item = frappe.db.get_single_value('Facility Management Settings', 'rental_item')
	submit_si = frappe.db.get_single_value('Facility Management Settings', 'submit_si')
	debit_to = get_debit_to()

	for item in items:
		invoice_data = make_data(item)
		items = invoice_data.pop('items')

		invoice = frappe.new_doc('Sales Invoice')
		invoice.update(invoice_data)
		invoice.append('items', items[0])
		invoice.set_missing_values()
		invoice.save()

		if submit_si:
			invoice.submit()

		set_invoice_created(item.name, invoice.name)


def _delink_sales_invoices(renting):
	sales_invoices = frappe.get_all('Sales Invoice', filters={'pm_rental_contract': renting.name})
	for sales_invoice in sales_invoices:
		frappe.db.set_value('Sales Invoice', sales_invoice, 'pm_rental_contract', '')


def _set_property_as_vacant(renting):
	retain_rental_on_cancel = frappe.db.get_single_value('Facility Management Settings', 'retain_rental_on_cancel')
	if not retain_rental_on_cancel:
		frappe.db.set_value('Property', renting.property, 'rental_status', 'Vacant')


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


def _get_invoice_on_start_date():
	return frappe.db.get_single_value('Facility Management Settings', 'invoice_on_start_date')
