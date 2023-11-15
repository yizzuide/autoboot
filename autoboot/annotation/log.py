
from functools import wraps
from time import perf_counter
from typing import Any, Callable

from autoboot.applications import AutoBoot


def log_time(fn) -> Callable[..., Any]:
  @wraps(fn)
  def decorator(*args, **kwargs) -> Any:
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