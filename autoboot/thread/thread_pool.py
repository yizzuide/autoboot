
from concurrent.futures import ThreadPoolExecutor
from autoboot.meta import Component
from autoboot import ServerProperties
from typing import Callable, Any


class ThreadPoolTask(Component):
  """The ThreadPoolTask class is extends Component which means is a singleton instance."""
  
  component_name = "thread_pool_task"
  
  def __init__(self):
    self.executor = ThreadPoolExecutor(max_workers=ServerProperties.thread_max_workers())
    
  def worker_size(self):
    return len(self.executor._threads)
  
  def queue_size(self):
    return self.executor._work_queue.qsize()
  
  def is_overflow(self):
    return (self.queue_size() + 1) > ServerProperties.thread_max_queue()
    
  def submit(self, fn: Callable[..., Any]):
    rejected = ServerProperties.thread_rejected()    
    if self.is_overflow():
      if rejected == "abort":
        raise RuntimeError("ThreadPoolTask: Too many task executing")
      elif rejected == "discard":
        return
    return self.executor.submit(fn)
  
  def shutdown(self):
    self.executor.shutdown(wait=True)
    
  def __call__(self, fn: Callable[..., Any]):
    return self.submit(fn)
    
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    self.shutdown()
    
  def __del__(self):
    self.shutdown()
    
  def __repr__(self):
    return f"ThreadPoolTask(size={self.worker_size()}, queue={self.queue_size()})"

  def __str__(self):
    return f"ThreadPoolTask(size={self.worker_size()}, queue={self.queue_size()})"