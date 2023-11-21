from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

T = TypeVar('T')

@dataclass
class Event(Generic[T]):
  source: any
  data: T
  

class EventEmitter(object):
  """
  EventEmitter is a class that allows you to register event listeners and
  emit events.
  """

  def __init__(self):
    self._listeners = {}

  def on(self, action):
    """
    Register a callback for an event.
    """
    
    def decorator(fn):
        self._listeners.setdefault(action, []).append(fn)
        return fn
    return decorator

  def emit(self, action, event: Event[T]):
    """
    Emit event with action
    """
    
    for f in self._listeners.get(action, []):
      f(event)
      
  def clear(self):
    self._listeners.clear()