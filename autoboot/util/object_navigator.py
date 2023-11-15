
from typing import Any


def get_value_by(dict: dict[str, Any], keypath: str) -> str | None:
    """
    Get the value of a keypath in a dictionary.

    Args:
        dict (dict): The dictionary to get the value from.
        keypath (str): The keypath to get the value from.

    Returns:
        str: The value of the keypath.
    """
    keys = keypath.split(".")
    value = dict
    for key in keys:
        value = value.get(key)
        if value is None:
            return None
    return value