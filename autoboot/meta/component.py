
from typing import Self
from autoboot.annotation.component import comp_from_cache
from .component_metaclass import ComponentMetaclass


class Component(metaclass=ComponentMetaclass):
  """Cache component and register it in IoC."""

  def __new__(cls) -> Self:
    """Create a new instance of the component."""
    _parent = super()
    return comp_from_cache(cls.__component_name__, lambda: _parent.__new__(cls))
  