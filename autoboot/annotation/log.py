
from functools import wraps
from time import perf_counter
from typing import Callable, TypeVar
from autoboot.applications import AutoBoot

R = TypeVar("R")

def log_time(fn: Callable[..., R]) -> R:
  @wraps(fn)
  def decorator(*args, **kwargs) -> R:
    start = perf_counter()
    try:
      result = fn(*args, **kwargs)
      end = perf_counter()
      duration = end - start
      AutoBoot.logger.debug(f"{fn.__name__} took {duration:4f} seconds to execute")
      return result
    except Exception as e:
      AutoBoot.logger.exception(f"exception happen with msg: {e}")
  return decorator
