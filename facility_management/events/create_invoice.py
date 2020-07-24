import frappe
from frappe.utils.data import today


def execute():
    tenant_dues = _get_tenant_dues()
    rental_item = frappe.db.get_single_value('Facility Management Settings', 'rental_item')

    for tenant_due in tenant_dues:
        tenant = tenant_due.get('tenant')
        description = tenant_due.get('description')
        rental_amount = tenant_due.get('rental_amount')
        advance_paid_amount = tenant_due.get('advance_paid_amount')

        amount = advance_paid_amount if description == 'Advance Payment' else rental_amount

        invoice = frappe.new_doc('Sales Invoice')
        invoice.update({
            'customer': frappe.db.get_value('Tenant', tenant, 'customer'),
            'posting_date': tenant_due.get('invoice_date'),
            'due_date': tenant_due.get('invoice_date'),
            'debit_to': frappe.db.get_value('Company', invoice.company, 'default_receivable_account'),
        })
        invoice.append('items', {
            'item_code': rental_item,
            'rate': amount,
            'qty': 1.0,
        })
        invoice.set_missing_values()
        invoice.save()

        _set_invoice_created(tenant_due.get('name'), invoice.name)


def _set_invoice_created(name, invoice_ref):
    frappe.db.set_value('Rental Contract Item', name, 'is_invoice_created', 1)
    frappe.db.set_value('Rental Contract Item', name, 'invoice_ref', invoice_ref)


def _get_tenant_dues():
    """
    Get due invoices during the day
    :return:
    """
    return frappe.db.sql("""
        SELECT
            `tabRental Contract Item`.name,
            `tabRental Contract Item`.invoice_date,
            `tabRental Contract Item`.description,
            `tabRental Contract`.rental_amount,
            `tabRental Contract`.advance_paid_amount,
            `tabRental Contract`.tenant
        FROM `tabRental Contract Item` INNER JOIN `tabRental Contract`
        ON `tabRental Contract Item`.parent = `tabRental Contract`.name
        WHERE `tabRental Contract`.docstatus = 1 
        AND `tabRental Contract Item`.is_invoice_created = 0
        AND `tabRental Contract Item`.invoice_date < %s
    """, today(), as_dict=True)
