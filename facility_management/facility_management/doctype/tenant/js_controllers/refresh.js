function refresh(frm) {
    frm.trigger('tenant_type');
    if (!frm.doc.__islocal) {
        erpnext.utils.set_party_dashboard_indicators(frm);
    }
}
