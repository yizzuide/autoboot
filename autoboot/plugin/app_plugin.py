
import abc


class AppPlugin(abc.ABC):
  
  @abc.abstractmethod
  def install(self) -> None:
    pass
  
  @abc.abstractmethod
  def env_prepared(self) -> None:
    pass
  
  @abc.abstractmethod
  def app_started(self) -> None:
    pass