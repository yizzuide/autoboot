
from autoboot.annotation.component import comp_from_cache


class Component(type):
  """Cache component and register it in IoC."""
  
  def __init__(cls, name, bases, attrs):
    super().__init__(name, bases, attrs)
        
  def __new__(cls, name: str, bases, classdict: dict):
    cls.__component_name__ = name
    return comp_from_cache(name, lambda: type.__new__(cls, name, bases, classdict))