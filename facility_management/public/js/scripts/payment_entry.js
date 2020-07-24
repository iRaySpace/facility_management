frappe.ui.form.on('Payment Entry', {
    refresh: function(frm) {
        _set_route_options(frm);
    }
});


function _set_route_options(frm) {
    if (frappe.__route_options) {
        Object.entries(frappe.__route_options).forEach(function(route_option) {
            if (['party', 'paid_amount'].includes(route_option[0])) { // because party and paid_amount
                setTimeout(() => frm.set_value(route_option[0], route_option[1]), 500);
            }
            frm.set_value(route_option[0], route_option[1]);
        });
        frappe.__route_options = null;
    }
}