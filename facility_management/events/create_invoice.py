import frappe
from frappe.utils.data import today


def execute():
    tenant_dues = _get_tenant_dues()
    rental_item = frappe.db.get_single_value('Facility Management Settings', 'rental_item')

    for tenant_due in tenant_dues:
        customer = frappe.db.get_value('Tenant', tenant_due.get('tenant'), 'customer')
        invoice = frappe.new_doc('Sales Invoice')
        invoice.update({
            'customer': customer,
            'due_date': tenant_due.get('invoice_date')
        })
        invoice.append('items', {
            'item_code': rental_item,
            'rate': tenant_due.get('rental_amount'),
            'qty': 1.0,
        })
        invoice.set_missing_values()
        invoice.save()

        _set_invoice_created(tenant_due.get('name'), invoice.name)


def _set_invoice_created(name, invoice_ref):
    frappe.db.set_value('Tenant Renting Item', name, 'is_invoice_created', 1)
    frappe.db.set_value('Tenant Renting Item', name, 'invoice_ref', invoice_ref)


def _get_tenant_dues():
    """
    Get due invoices during the day
    :return:
    """
    return frappe.db.sql("""
        SELECT
            `tabTenant Renting Item`.name,
            `tabTenant Renting Item`.invoice_date,
            `tabTenant Renting Item`.description,
            `tabTenant Renting`.rental_amount,
            `tabTenant Renting`.advance_paid_amount,
            `tabTenant Renting`.tenant
        FROM `tabTenant Renting Item` INNER JOIN `tabTenant Renting`
        ON `tabTenant Renting Item`.parent = `tabTenant Renting`.name
        WHERE `tabTenant Renting`.docstatus = 1 
        AND `tabTenant Renting Item`.is_invoice_created = 0
        AND `tabTenant Renting Item`.invoice_date <= %s
    """, today(), as_dict=True)
