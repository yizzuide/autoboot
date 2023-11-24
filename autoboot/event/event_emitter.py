from dataclasses import dataclass
from typing import TypeVar, Generic, Callable
from autoboot.util.type_reflect import get_generic_type

T = TypeVar('T')

@dataclass
class Event(Generic[T]):
  data: T
  source: any = None
  

class EventEmitter(object):
  """
  EventEmitter is a class that allows you to register event listeners and
  emit events.
  """

  def __init__(self):
    self._listeners = {}

  def on(self, action="default"):
    """
    Register a callback for an event with action name.
    """
    
    def decorator(fn: Callable[..., None], *args, **kwargs) -> None:
      self._listeners.setdefault(action, []).append(fn)
    return decorator
  
  def on_event(self, fn: Callable[..., None]):
    """
    Register a callback for an event with event generic type.
    """
    
    self._listeners.setdefault("default", []).append(fn)
    

  def emit(self, event: Event[T], action = "default"):
    """
    Emit event with action
    """
    
    check_type = action == "default"
    for f in self._listeners.get(action, []):
      if not check_type:
        f(event)
      else:
        generic_type = get_generic_type(f, "event", 0)
        if generic_type and isinstance(event.data, generic_type):
          f(event)
      
  def clear(self):
    self._listeners.clear()