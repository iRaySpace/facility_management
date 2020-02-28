# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.data import add_to_date


class TenantRenting(Document):
	def validate(self):
		self.auto_invoice_date = add_to_date(self.contract_start_date, months=3)
