
from functools import wraps
from time import perf_counter
from typing import Any, Callable
import wrapt
import loguru
from autoboot.applications import AutoBoot
from autoboot.logging import Logging


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

def log_catch(fn, user_case: str = "catch") -> Callable[..., Any]:
  """
  Add error catch log with loguru.
  """
  Logging.catch_file_rotation_logger(user_case=user_case)
  @wrapt.decorator
  @loguru.catch
  def decorator(fn, instance, args, kwargs) -> Any:
    return fn(*args, **kwargs)
  return decorator