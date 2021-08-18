from .errors import InvalidCredential
from typing import Any, List
from uuid import UUID


def get(__list: List[dict], key: str, value: Any) -> dict:
    """Finds an element from a list of dictionaries with a key and value."""
    for __dict in __list:
        if __dict.get(key).lower() == value:
            return __dict
    return False


def is_valid_uuid(uuid: str) -> UUID:
    try:
        return UUID(uuid, version=4)
    except ValueError:
        raise InvalidCredential


__all__ = (
    "get",
    "is_valid_uuid"
)
