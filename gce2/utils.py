from typing import Any


def _is_str(object: Any) -> bool:
    """Verify if object can be transform to string"""
    try:
        str(object)
    except Exception:
        return False
    else:
        return True


def _is_int(object: Any) -> bool:
    """Verify if object can be transform to integer"""
    try:
        int(object)
    except Exception:
        return False
    else:
        return True
