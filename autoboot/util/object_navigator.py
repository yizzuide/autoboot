
import re
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


def extract_json(json_data, keypath):
  """
    Extracts data from a JSON object using a dot ('.') for object navigation and square brackets ('[]') for array navigation.
    For example: "person.name", "array[2].value", "items.2.value"
    
    Args:
      json_data: The JSON object as a Python dictionary.
      keypath: The keypath to the desired data, using '.' and '['/']' notation. 
    
    Returns:
        The extracted data, or None if the keypath is invalid.
    """
  parts = re.split(r'\.|\[', keypath)
  parts = [part.rstrip(']') for part in parts if part]
  current = json_data
  for part in parts:
      if isinstance(current, dict):
          if part not in current:
              return None
          current = current[part]
      elif isinstance(current, list):
          try:
              index = int(part)
              if index < 0 or index >= len(current):
                  return None
              current = current[index]
          except ValueError:
              return None
      else:
          return None
  return current