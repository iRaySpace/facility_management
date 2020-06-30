function set_full_name(frm) {
    const full_name = [
        frm.doc.first_name,
        frm.doc.last_name,
    ];
    frm.set_value('tenant_name', full_name.join(' '));
}
