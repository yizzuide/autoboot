
import abc
from typing import TypeVar, Generic

from autoboot import AutoBoot
from .app_plugin_metaclass import AppPluginMetaclass

T = TypeVar('T')

class AppPlugin(Generic[T], metaclass=AppPluginMetaclass):
  """An abstract class used to extends for add to framework."""
  
  @classmethod
  def get_context(cls) -> T:
    """Don't override this class method which used by the internal mechanism of the framework."""
    return AutoBoot.get_runner(cls.__ctx__)
  
  @classmethod
  def get_context_name(cls) -> str:
    """Don't override this class method which used by the internal mechanism of the framework."""
    return cls.__ctx__
  
  @abc.abstractmethod
  def install(self) -> T:
    """Install plugin and return runner context."""
    pass
  
  @abc.abstractmethod
  def env_prepared(self) -> None:
    """Invoke after env vars prepared. 
    
    it should be noted that current runner context not created.
    """
    pass
  
  @abc.abstractmethod
  def app_started(self) -> None:
    """Invoke after application started success."""
    pass