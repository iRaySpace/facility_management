# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class RealEstateProperty(Document):
	def validate(self):
		_validate_abbr(self)


def _validate_abbr(property):
	if not property.abbr:
		property.abbr = ''.join([c[0] for c in property.name.split()]).upper()

	property.abbr = property.abbr.strip()

	if not property.abbr:
		frappe.throw(_("Abbreviation is mandatory"))

	if frappe.get_all('Real Estate Property', filters=[['abbr', '=', property.abbr], ['name', '!=', property.name]]):
		frappe.throw(_("Abbreviation already used for another property"))
