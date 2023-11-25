from functools import wraps
from typing import Callable, TypeVar
from loguru import logger
from autoboot.applications import AutoBoot

R = TypeVar("R")

def comp_from_cache(name: str, comp_factory: Callable[..., R]):
  """
  Get component from cache
  """
 
  app: AutoBoot = AutoBoot.instance()
  # return cached component if match
  for key, comp in app.components:
    if key == name:
      return comp
  comp = comp_factory()
  # caching component with name
  if comp:
    app.components.append((name, comp))
    (AutoBoot.logger or logger).info(f"component cached: {name}")
  return comp

def component(name: str):
  """register as a component which cached with name for next time get"""
  def wrapper(fn: Callable[..., R]) -> Callable[..., R]:
    @wraps(fn)
    def decorator(*args, **kwargs) -> R:
      return comp_from_cache(name, lambda: fn(*args, **kwargs))
    return decorator
  return wrapper


""" define component using class style
class Component:
  def __init__(self, name: str):
    self.name = name
    
  def __call__(self, fn: Callable[..., R]) -> Callable[..., R]:
    @wraps(fn)
    def decorator(*args, **kwargs) -> R:
      app: AutoBoot = AutoBoot.instance()
      # return cached component if match
      for key, comp in app.components:
        if key == self.name:
          return comp
      result = fn(*args, **kwargs)
      # caching component with name
      if result:
        app.components.append((self.name, result))
        (AutoBoot.logger or logger).info(f"component cached: {self.name}")
      return result
    return decorator 
"""
