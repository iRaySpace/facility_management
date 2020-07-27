import frappe


def execute():
    frappe.delete_doc_if_exists('Custom Field', 'Sales Invoice-pm_tenant_renting')
