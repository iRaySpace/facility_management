function prompt_log() {
    return new Promise(function(resolve, reject) {
        const dialog = new frappe.ui.Dialog({
            title: 'Log History',
            fields: [
                {
                    fieldname: 'datetime',
                    fieldtype: 'Datetime',
                    label: __('Activity Datetime'),
                },
                {
                    fieldname: 'status',
                    fieldtype: 'Select',
                    label: __('Status'),
                    options: ['Work in Progress', 'Awaiting Parts'],
                },
                {
                    fieldname: 'description',
                    fieldtype: 'Small Text',
                    label: __('Description'),
                },
            ]
        });
        dialog.set_primary_action('Submit & Log', function() {
            dialog.hide();
            resolve(dialog.get_values());
        });
        dialog.show();
    });
}
