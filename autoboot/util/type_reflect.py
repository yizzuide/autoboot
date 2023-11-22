import inspect
from typing import Any, Callable, get_args


def has_property(obj: Any, prop: str, is_own: bool) -> bool:
  """
  Checks if a property is present in an object.

  Args:
    obj(Any): The object to check.
    prop(str): The property to check.
    is_own(bool): Whether to check the object's own properties or all properties.
    
  Returns:
    bool: True if the property is present, False otherwise.
  """
  if is_own:
    # properties from object.__dict__
    return prop in vars(obj)
  else:
    # properties from self or super class
    return hasattr(obj, prop)
  
def get_method_params(fn: Callable[..., Any]):
  return inspect.signature(fn).parameters

def get_param_generic(param: inspect.Parameter, index: int):
  return get_args(param.annotation)[index]

def get_generic_type(fn: Callable[..., Any], param_name: str, index: int):
  params = get_method_params(fn)
  event_param = params.get(param_name)
  return get_param_generic(event_param, index) if event_param else None

def match_param_type(param: inspect.Parameter, type: Any):
  return param.annotation == type
