import tablib


def excel(format_string, headers, data_lines):
    data = tablib.Dataset(headers=headers)
    for i in data_lines:
        data.append(i)
    return data.export(format_string)

