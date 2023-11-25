
from typing import Self
from autoboot.annotation.component import comp_from_cache


class Component:
  """Cache component and register it in IoC."""

  def __new__(cls) -> Self:
    cls.__component_name__ = cls.__name__
    _parent = super()
    return comp_from_cache(cls.__name__, lambda: _parent.__new__(cls))
  