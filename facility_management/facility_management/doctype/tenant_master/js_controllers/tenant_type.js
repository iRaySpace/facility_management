function tenant_type(frm) {
    frm.set_df_property('tenant_name', 'read_only', frm.doc.tenant_type === 'Individual');
    frm.set_df_property('first_name', 'hidden', frm.doc.tenant_type === 'Company');
    frm.set_df_property('last_name', 'hidden', frm.doc.tenant_type === 'Company');
    frm.set_df_property('first_name', 'reqd', frm.doc.tenant_type === 'Individual');
    frm.set_df_property('last_name', 'reqd', frm.doc.tenant_type === 'Individual');
}


