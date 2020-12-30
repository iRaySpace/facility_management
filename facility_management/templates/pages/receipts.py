import frappe
from toolz import first


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = True

    name = frappe.form_dict.name
    if name:
        context.row = frappe.get_doc("Payment Entry", name)
    else:
        customer = _get_customer(frappe.session.user)
        context.data = _get_data(customer)


def _get_data(party):
    return frappe.get_all(
        "Payment Entry",
        fields=[
            "name",
            "posting_date",
            "status",
            "paid_amount",
        ],
        filters={"party": party},
    )


def _get_customer(user):
    customer = frappe.db.sql(
        """
            SELECT dl.link_name
            FROM `tabContact` c
            INNER JOIN `tabDynamic Link` dl ON dl.parent = c.name
            WHERE dl.link_doctype = "Customer" AND c.user = %s
        """,
        user,
        as_dict=1,
    )
    return first(customer).get("link_name") if customer else None


def _get_tenant(customer):
    tenant = frappe.get_all("Tenant Master", filters={"customer": customer})
    return first(tenant).get("name") if tenant else None
