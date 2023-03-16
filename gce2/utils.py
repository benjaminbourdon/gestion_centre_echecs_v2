def _is_str(object):
    try:
        str(object)
    except Exception:
        return False
    else:
        return True


def _is_int(object):
    try:
        int(object)
    except Exception:
        return False
    else:
        return True
