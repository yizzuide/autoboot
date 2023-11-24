from functools import wraps
from time import sleep
from typing import TypeVar, Callable
from result import Ok, Err, Result
from loguru import logger
  
R = TypeVar("R")
  
def retry(tries: int, delay: float, exceptions: type[Exception] | tuple[type[Exception], ...] = BaseException):
  """
  Retry a function if it fails.
  """
  
  def wrapper(fn: Callable[..., R]) -> Callable[..., Result[R, str]]:
    @wraps(fn)
    def decorator(*args, **kwargs) -> Result[R, str]:
      for i in range(tries):
        try:
          return Ok(fn(*args, **kwargs))
        except exceptions as e:
          logger.exception(f"Retrying {fn.__name__} after exception:")
          if i < tries - 1:
            sleep((i * delay) ** i)
          else:
            return Err(str(e))
    return decorator
  return wrapper