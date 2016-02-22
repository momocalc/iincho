def maximum(list_val):
    '''
    get the maximum value from a list
    '''

    return max(list_val)


def minimum(list_val):
    '''
    get the minimum value from a list
    '''
    return min(list_val)


def datetimeformat(value, format='%Y/%m/%d %H:%M:%S'):
    return value.strftime(format)


def remove_param_str(q, key):
    _q = q.copy()

    if _q.get(key) != None:
        _q.pop(key)

    return _q


def update_param_str(q, values, copy=True):
    _q = q.copy() if copy else q

    for key in values.keys():
        if _q.get(key) != None:
            _q.pop(key)

    _q.update(values)
    return _q
