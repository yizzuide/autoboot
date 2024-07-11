
import wrapt
from functools import wraps
from typing import Callable, Optional, TypeVar
from loguru import logger

from autoboot.applications import AutoBoot
from .env import env, value


R = TypeVar("R")

def comp_from_cache(name: str, comp_factory: Callable[..., R]):
  """
  Get component from cache
  """
  
  app = AutoBoot.instance()
  # return cached component if match
  for key, comp in app.components:
    if key == name:
      return comp
  comp = comp_factory()
  
  for listener in app._component_listeners:
    listener.after_instantiation(name, comp)
    
  # caching component with name
  if comp:
    app.components.append((name, comp))
    (AutoBoot.logger or logger).info(f"component cached: {name}")
  return comp

def value_component(keypath: str) -> R:
  """get value from config file and cache as component."""
  
  @wrapt.decorator
  @component(f"env[{keypath}]")
  def decorator(fn: Callable[..., R], instance, args, kwargs) -> R:
    return env(keypath) or fn(*args, **kwargs)
  return decorator

def static_property(keypath: str) -> R:
  """Decorate as a static method, get value from config file and cache as component.

  Args:
      keypath (str): config key name

  Returns:
      R: config value
  """ 
  
  # @staticmethod not work with @wrapt.decorator
  def wrapper(fn: Callable[..., R]) -> R:
    @staticmethod
    @component(f"env[{keypath}]")
    @value(keypath)
    @wraps(fn)
    def decorator(*args, **kwargs):
        return fn(*args, **kwargs)
    return decorator
  return wrapper

def component(name: Optional[str] = None) -> Callable[..., R]:
  """register as a component which cached with name."""
  
  def wrapper(fn: Callable[..., R]) -> Callable[..., R]:
    @wraps(fn)
    def decorator(*args, **kwargs) -> R:
      comp_name = fn.__name__ if name is None else name
      return comp_from_cache(comp_name, lambda: fn(*args, **kwargs))
    return decorator
  return wrapper

def conditional(value: str, having_value: bool | str, match_if_missing: bool = False):
  """Check env[value] match the having_value before register as component with @component()."""
  
  def wrapper(fn: Callable[..., R]) -> Callable[..., R]:
    @wraps(fn)
    def decorator(*args, **kwargs) -> R:
      if env(value) == having_value or match_if_missing:
        return fn(*args, **kwargs)
      else:
        return None
    return decorator
  return wrapper

class Component:
  """register as a component which cached with name."""
  
  def __init__(self, name: str):
    self.name = name
    
  def __call__(self, fn: Callable[..., R]) -> Callable[..., R]:
    @wraps(fn)
    def decorator(*args, **kwargs) -> R:
      return comp_from_cache(self.name, lambda: fn(*args, **kwargs))
    return decorator
