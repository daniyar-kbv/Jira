def find_type(tuple, index):
    type_name = [item[1] for item in tuple if item[0] == index][0]
    if isinstance(type_name, (type(''))) and type_name != '':
        return type_name
    return ''