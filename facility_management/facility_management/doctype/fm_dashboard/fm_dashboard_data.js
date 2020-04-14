async function get_rental_listing() {
  const { message: rental_listing } = await frappe.call({
    method: 'facility_management.api.tenant_renting.get_rental_listing'
  });
  return rental_listing;
}
