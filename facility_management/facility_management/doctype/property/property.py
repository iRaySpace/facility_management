# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class Property(Document):
	def validate(self):
		_validate_property_status(self)
		_validate_abbr(self)


def _validate_property_status(property):
	if property.property_status == 'Rental' and not property.rental_status:
		frappe.throw(_('Please set Rental Status as Vacant or Rented'))


def _validate_abbr(property):
	if not property.abbr:
		property.abbr = ''.join([c[0] for c in property.property_group.split()]).upper() + property.property_no

	property.abbr = property.abbr.strip()

	if not property.abbr:
		frappe.throw(_("Abbreviation is mandatory"))

	if frappe.db.sql("SELECT abbr FROM `tabProperty` WHERE abbr=%s", property.abbr):
		frappe.throw(_("Abbreviation already used for another property"))
