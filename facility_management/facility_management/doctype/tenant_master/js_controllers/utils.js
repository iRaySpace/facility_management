function set_full_name(frm) {
    frm.set_value('tenant_name', `${frm.doc.first_name} ${frm.doc.last_name}`);
}
