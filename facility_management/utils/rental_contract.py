from facility_management.api.property import get_property_name


def make_description(data):
    return " ".join([
        "Rental for",
        data.get("posting_date").strftime("%b %Y"),
        f"for property {get_property_name(data.get('property'))} as per contract {data.get('rental_contract')}"
    ])
