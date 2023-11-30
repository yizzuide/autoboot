
from typing import Protocol, Any, runtime_checkable

@runtime_checkable
class ComponentListener(Protocol):
  
  def after_instantiation(self, name: str, component: Any):...