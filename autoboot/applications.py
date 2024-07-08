
import loguru
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple, TypeVar, Self
from autoboot.args import get_env_name
from autoboot.logging import Logging
from autoboot.plugin import AppPlugin
from autoboot.process import load_env_file, load_yaml_file
from autoboot.event import ApplicationListener
from autoboot.event import ComponentListener

# define AutoBoot class type
AppType = TypeVar("AppType", bound="AutoBoot")

R = TypeVar("R")

# In Python 3.10+ you can use `slots=True` with a dataclass to make it more memory-efficient.
@dataclass(slots=True)
class AutoBootConfig:
  """AutoBoot global config"""
  
  # show detail log
  verbose: bool = False
  # config dir path which relative to the current project
  config_dir: str = "."
  # yaml config name, it support `.yml` and `.yaml`
  yml_config: str = "autoboot"
  
  

class AutoBoot(object):
  """The root application context which use of single containers is designed for simplicity and microservice."""
  
  _instance = None
  _init_flag = False
  
  def __new__(cls, config: Optional[AutoBootConfig] = AutoBootConfig()) -> Self:
    # create instance only once
    if cls._instance is None:
        cls._instance = super().__new__(cls)
    return cls._instance
  
  def __init__(self, config: Optional[AutoBootConfig] = AutoBootConfig()) -> None:
    if AutoBoot._init_flag is True:
      return
    self.config = config
    self._app_plugins: list[AppPlugin] = []
    self._components: list[Tuple[str, Any]] = []
    self._component_listeners: list[ComponentListener] = []
    self._runners: dict[str, Any] = {}
    self._listeners: list[ApplicationListener] = []
    self._config_data = dict[str, Any]
    AutoBoot.logger: loguru.Logger = None
    AutoBoot._init_flag = True
    
  @classmethod
  def instance(cls):
    """Return current application context instance."""
    return cls._instance
  
  @classmethod
  def get_config_data(cls) -> dict[str, Any]:
    """Get yaml config dict data."""
    return cls.instance()._config_data
  
  @staticmethod
  def get_runner(name: str):
    """Get plugin runner with name."""
    return AutoBoot.instance()._runners.get(name)
  
  @property
  def app_plugins(self) -> list[AppPlugin]:
    """Get application plugins."""
    return self._app_plugins
  
  @app_plugins.setter
  def app_plugins(self, app_plugins: list[AppPlugin]) -> None:
    self._app_plugins = app_plugins
  
  @property
  def components(self) -> list[Tuple[str, Any]]:
    """Ioc container for find depends."""
    return self._components
    
  def apply(self, app_plugin: AppPlugin) -> Self:
    """Apply plugin in application context."""
    self._app_plugins.append(app_plugin)
    return self
    
  def addListener(self, listener: ApplicationListener) -> Self:
    self._listeners.append(listener)
    return self
  
  def addComponentListener(self, listener: ComponentListener) -> Self:
    self._component_listeners.append(listener)
    return self
  
  def run(self, expose: Callable[..., R] = None):
    """Application context run entry."""
    
    # config environment variables
    env_name = get_env_name()
    
    # load .env
    load_env_file(self.config.config_dir, env_name)
    
    # load yml
    self._config_data = load_yaml_file(self.config.config_dir, self.config.yml_config)
    
    # config logger
    from autoboot.application_properties import ApplicationProperties
    AutoBoot.logger = Logging(
      app_name=ApplicationProperties.app_name(),
      module=ApplicationProperties.module(),
      level=ApplicationProperties.log_level(),
      log_dir=ApplicationProperties.log_dir(),
      max_size=ApplicationProperties.log_max_size(),
      retention=ApplicationProperties.log_retention(),
      env_name=env_name
    ).logger
    
    AutoBoot.logger.info(f"application finish load env: {env_name}")
    
    for ap in self.app_plugins:
      ap.env_prepared()
      
    for listener in self._listeners:
      listener.on_env_prepared(self._config_data)
      
    for ap in self.app_plugins:
      runner = ap.install()
      self._runners[ap.get_context_name()] = runner
      
    if ApplicationProperties.scan_listener_packages():
      for package in ApplicationProperties.scan_listener_packages():
        __import__(package)

    for ap in self.app_plugins:
      ap.app_started()
      
    for listener in self._listeners:
      listener.on_started()
      
    AutoBoot.logger.info("application started!")
    
    if expose:
      return expose()