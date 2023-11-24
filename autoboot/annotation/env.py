
import os
import wrapt
from typing import Callable, TypeVar
from autoboot.applications import AutoBoot
from autoboot.annotation.component import component
from autoboot.process import get_yml_value

R = TypeVar("R")

def env(keypath: str) -> int | float | str | dict | list | None:
  """get env value from keypath, support find in `.env` and `.yml`."""
  
  if "." in keypath:
    value = get_yml_value(AutoBoot.get_config_data(), keypath=keypath)
    if not value:
      return None
    return value
  else:
    value = os.getenv(keypath)
    if value:
      return value
    value = AutoBoot.get_config_data().get(keypath)
    return value if value else None
    

def value(keypath: str) -> R:
  """get value from config file."""
  
  @wrapt.decorator
  def decorator(fn: Callable[..., R], instance, args, kwargs) -> R:
    return env(keypath) or fn(*args, **kwargs)
  return decorator
      

def value_component(keypath: str) -> R:
  """get value from config file and cache as component."""
  
  @wrapt.decorator
  @component(name=f"env[{keypath}]")
  def decorator(fn: Callable[..., R], instance, args, kwargs) -> R:
    return env(keypath) or fn(*args, **kwargs)
  return decorator