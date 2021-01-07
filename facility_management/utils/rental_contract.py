from facility_management.api.property import get_property_name


def make_description(data):
    return " ".join([
        data.get("posting_date").strftime("%b %Y"),
        f"for {get_property_name(data.get('property'))} as per {data.get('rental_contract')}"
    ])
