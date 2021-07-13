def get(_list, key, value):
    for _dict in _list:
        if _dict[key] == value:
            return _dict
    return False