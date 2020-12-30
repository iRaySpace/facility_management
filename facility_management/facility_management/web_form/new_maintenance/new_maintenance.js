frappe.ready(function() {
  frappe.web_form.events.on("after_load", function() {
    const properties = {{ properties|tojson|safe }};
    _set_options("property", properties);
  });
});

function _set_options(fieldname, options) {
  const field = frappe.web_form.get_field(fieldname);
  field.df.options = options;
  field.refresh();
}
