
from autoboot.annotation.env import value_component

class ServerProperties:

  @value_component("server.threads.max")
  @staticmethod
  def thread_max_workers() -> int:
    """The max workers is 31"""
    return 28
  
  @value_component("server.threads.queue_size")
  @staticmethod
  def thread_max_queue() -> int:
    """The max queue is 1000"""
    return 1000
  
  @value_component("server.threads.rejected")
  @staticmethod
  def thread_rejected() -> str:
    """Available reject strategy: abort, discard, wait"""
    return "wait"