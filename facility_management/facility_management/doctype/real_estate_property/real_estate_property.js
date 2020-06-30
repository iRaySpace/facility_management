// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Real Estate Property', {
    onload: function(frm) {
        frm.set_query('cost_center', function() {
            return {
                filters: { is_group: 0 },
            };
        });
    },
	insured: function(frm) {
		// TODO: commons
		const reqd_fields = ['insurance_company', 'insurance_type', 'insurance_start_date', 'insurance_end_date'];
		reqd_fields.forEach((reqd_field) => frm.set_df_property(reqd_field, 'reqd', frm.doc.insured));
	}
});
