
from functools import wraps
from time import perf_counter
from typing import Callable, TypeVar
from loguru import logger
from autoboot.applications import AutoBoot
from autoboot.logging import Logging

R = TypeVar("R")

def log_time(fn: Callable[..., R]) -> R:
  """Debug function take time after run finish."""
  
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

def log_catch(user_case: str):
  """Add catch error log with loguru.

  A decorator add on function type, it used logger config.

  Args:
  user_case: set current user case
  """
  
  def wrapper(fn: Callable[..., R]) -> Callable[..., R]:
    @logger.catch
    @wraps(fn)
    def decorator(*args, **kwargs) -> R:
      Logging.catch_file_rotation_logger(user_case)
      return fn(*args, **kwargs)
    return decorator
  return wrapper
