from functools import reduce


def group_by(key, rows):
    def make_data(data, row):
        key_value = row.get(key)
        if key_value not in data:
            data[key_value] = []
        data[key_value].append(row)
        return data
    return reduce(make_data, rows, {})


def sum_by(key, rows):
    return reduce(lambda total, x: total + x[key], rows, 0.00)


def get_first_and_pluck_by(key, rows):
    filtered = list(filter(lambda x: x.get(key), rows))
    return filtered[0].get(key) if filtered else None


def concat_not_empty(a, not_empty):
    return a + not_empty if not_empty else None
