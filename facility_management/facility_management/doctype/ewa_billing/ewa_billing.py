# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from functools import reduce


class EWABilling(Document):
	def validate(self):
		_validate_total(self)


def _validate_total(billing):
	billing.total = reduce(lambda total, x: total + x.excess_amount, billing.items, 0.00)
