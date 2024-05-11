
from autoboot.annotation.env import static_property

class ServerProperties:

  @static_property("server.threads.max")
  def thread_max_workers() -> int:
    """The max workers is 31"""
    return 28
  
  @static_property("server.threads.queue_size")
  def thread_max_queue() -> int:
    """The max queue is 1000"""
    return 1000
  
  @static_property("server.threads.rejected")
  def thread_rejected() -> str:
    return "wait"