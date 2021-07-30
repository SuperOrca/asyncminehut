from typing import Any


def get(__list, key, value) -> Any:
    for __dict in __list:
        if __dict.get(key) == value:
            return __dict
    return False


__all__ = (
    "get"
)
