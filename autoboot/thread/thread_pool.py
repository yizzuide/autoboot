
from concurrent.futures import ThreadPoolExecutor
from autoboot.meta import Component
from autoboot import ServerProperties
from typing import Callable, Any


class ThreadPoolTask(Component):
  
  def __init__(self):
    self.executor = ThreadPoolExecutor(max_workers=ServerProperties.thread_max_workers())
    
  def worker_size(self):
    return self.executor._work_queue.qsize()
    
  def submit(self, fn: Callable[..., Any]):
    executing_tasks = self.worker_size()
    max_workers = ServerProperties.thread_max_workers()
    rejected = ServerProperties.thread_rejected()
    
    if executing_tasks > max_workers:
      if rejected == "abort":
        raise RuntimeError("ThreadPoolExecute: Too many threads executing")
      elif rejected == "discard":
        return
      
    self.executor._work_queue.put(fn)
        