import threading
import weakref
from typing import Union, TypeVar, Generic

T = TypeVar("T")

class ThreadLocal(Generic[T]): 
  
  def __init__(self) -> None:
    self.localMap = weakref.WeakValueDictionary()
    self.lock = threading.RLock()
    
  
  def set(self, key: Union[str, int], value: T) -> None:
    with self.lock:
      self.localMap[key] = value
  
  def get(self, key: str | int) -> T:
    with self.lock:
      return self.localMap.get(key)
    
  def clear(self, key: str | int) -> None:
    with self.lock:
      self.localMap.pop(key, None)