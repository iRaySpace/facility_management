async function get_items(property_name) {
    const { message: items } = await frappe.call({
        method: 'facility_management.api.property_checkup.get_items',
        args: { property_name },
    });
    return items;
}
