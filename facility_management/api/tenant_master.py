import json
import frappe
from frappe import _
from toolz import first


@frappe.whitelist()
def edit_personal_info(data):
    data = json.loads(data)
    tenant = _get_tenant(_get_customer(frappe.session.user))
    tenant.update(data)
    tenant.save(ignore_permissions=True)
    return True


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
    if tenant:
        return frappe.get_doc("Tenant Master", first(tenant).get("name"))
    else:
        frappe.throw(_("Tenant is not found"))
