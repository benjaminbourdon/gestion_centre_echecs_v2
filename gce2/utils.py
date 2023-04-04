def _is_str(object) -> bool:
    """Verify if object can be transform to string"""
    try:
        str(object)
    except ValueError:
        return False
    else:
        return True


def _is_int(object) -> bool:
    """Verify if object can be transform to integer"""
    try:
        int(object)
    except ValueError:
        return False
    else:
        return True
