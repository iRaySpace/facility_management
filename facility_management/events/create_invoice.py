import frappe
from frappe import _dict
from frappe.utils.data import today, get_first_day, get_last_day
from facility_management.helpers import set_invoice_created


# TODO: remove unused codes
def execute(**kwargs):
    rental_contract = kwargs.get('rental_contract', None)
    rental_contract_items = kwargs.pop('rental_contract_items', None)

    tenant_dues = _get_tenant_dues(kwargs)
    rental_item = frappe.db.get_single_value('Facility Management Settings', 'rental_item')
    submit_si = frappe.db.get_single_value('Facility Management Settings', 'submit_si')

    if not tenant_dues and rental_contract_items:
        tenant_dues = rental_contract_items

    for tenant_due in tenant_dues:
        if not isinstance(tenant_due, _dict):
            tenant_due = tenant_due.as_dict()

        tenant = tenant_due.get('tenant')
        description = tenant_due.get('description')
        rental_amount = tenant_due.get('rental_amount')
        advance_paid_amount = tenant_due.get('advance_paid_amount')
        customer = frappe.db.get_value('Tenant Master', tenant, 'customer')

        parent_rc = tenant_due.get('parent')
        if not parent_rc:
            parent_rc = rental_contract

        amount = advance_paid_amount if description == 'Advance Payment' else rental_amount

        invoice = frappe.new_doc('Sales Invoice')
        invoice.update({
            'customer': customer,
            'posting_date': get_first_day(tenant_due.get('invoice_date')),
            'posting_time': 0,
            'due_date': tenant_due.get('invoice_date'),
            'debit_to': frappe.db.get_value('Company', invoice.company, 'default_receivable_account'),
            'set_posting_time': 1,
            'pm_rental_contract': parent_rc
        })
        invoice.append('items', {
            'item_code': rental_item,
            'rate': amount,
            'qty': 1.0,
        })
        invoice.set_missing_values()
        invoice.save()

        if submit_si:
            invoice.submit()

        set_invoice_created(tenant_due.get('name'), invoice.name)


def _get_tenant_dues(filters):
    """
    Get due invoices during the day
    :return:
    """
    clauses = _get_clauses(filters)
    return frappe.db.sql(
        """
            SELECT
                rci.name,
                rci.invoice_date,
                rci.description,
                rci.parent,
                rc.rental_amount,
                rc.advance_paid_amount,
                rc.tenant
            FROM `tabRental Contract Item` rci
            INNER JOIN `tabRental Contract` rc
            ON rci.parent = rc.name
            WHERE rc.docstatus = 1 
            AND rci.is_invoice_created = 0
            {clauses}
        """.format(clauses='AND ' + clauses if clauses else ''),
        {
            **filters,
            'now': get_last_day(today())
        },
        as_dict=True
    )


def _get_clauses(filters):
    clauses = []
    if filters.get('rental_contract'):
        clauses.append('rc.name = %(rental_contract)s')
    if not filters.get('apply_now'):
        clauses.append('rci.invoice_date < %(now)s')
    return 'AND'.join(clauses)
