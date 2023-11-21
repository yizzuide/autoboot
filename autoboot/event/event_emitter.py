import inspect
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, get_args

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
    Register a callback for an event.
    """
    def decorator(fn: Callable[..., None]) -> None:
      self._listeners.setdefault(action, []).append(fn)
    return decorator

  def emit(self, event: Event[T], action = "default"):
    """
    Emit event with action
    """
    
    check_type = action == "default"
    for f in self._listeners.get(action, []):
      if not check_type:
        f(event)
      else:
        # get event param using inspect
        params = inspect.signature(f).parameters
        if params.get("event") is not None:
          # retrieval event data generic type using get_args
          generic_type = get_args(params.get("event").annotation)[0]
          if isinstance(event.data, generic_type):
            f(event)
      
  def clear(self):
    self._listeners.clear()