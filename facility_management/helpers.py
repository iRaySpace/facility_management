def get_status(status_conditions):
    for key, values in status_conditions.items():
        if all(values):
            return key
