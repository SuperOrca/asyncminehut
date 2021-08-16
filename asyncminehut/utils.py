from typing import Any, Dict, List


def get(__list: List, key: Any, value: Any) -> Dict:
    """Finds a element from a list of dictionaries with a key and value.

    Args:
        __list (List)
        key (Any)
        value (Any)

    Returns:
        Dict
    """
    for __dict in __list:
        if __dict.get(key) == value:
            return __dict
    return False


__all__ = (
    "get"
)
