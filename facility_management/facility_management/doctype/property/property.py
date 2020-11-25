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


def _validate_property_status(property):
	if property.property_status == 'Rental' and not property.rental_status:
		frappe.throw(_('Please set Rental Status as Vacant or Rented'))
