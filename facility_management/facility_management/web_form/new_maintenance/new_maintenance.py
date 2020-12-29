from __future__ import unicode_literals
from toolz import first
import frappe


def get_context(context):
    tenant = _get_tenant(_get_customer(frappe.session.user))
    context.properties = _get_properties(tenant)


def _get_properties(tenant):
    properties = frappe.get_all(
        "Rental Contract",
        fields=["property"],
        filters={"status": "Active", "tenant": tenant}
    )
    return list(map(lambda x: x.get("property"), properties))


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
