
import abc
from typing import TypeAlias, Any

Runner: TypeAlias = (str, Any)

class AppPlugin(abc.ABC):
  
  @staticmethod
  def get_context() -> Any:
    return
  
  @abc.abstractmethod
  def install(self) -> Runner:
    pass
  
  @abc.abstractmethod
  def env_prepared(self) -> None:
    pass
  
  @abc.abstractmethod
  def app_started(self) -> None:
    pass