
import loguru
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple, TypeVar
from autoboot.args import get_env_name
from autoboot.logging import Logging
from autoboot.plugin import AppPlugin
from autoboot.process import load_env_file, load_yaml_file

# define AutoBoot class type
AppType = TypeVar("AppType", bound="AutoBoot")

R = TypeVar("R")

@dataclass
class AutoBootConfig:
  """AutoBoot global config"""
  
  # show detail log
  verbose: bool = False
  # config dir path which relative to the current project
  config_dir: str = "."
  # yaml config name, it support `.yml` and `.yaml`
  yml_config: str = "autoboot"
  
  

class AutoBoot(object):
  """create instance of AutoBoot."""
  
  _instance = None
  _init_flag = False
  
  def __new__(cls, config: Optional[AutoBootConfig]) -> AppType:
    # create instance only once
    if cls._instance is None:
        cls._instance = super().__new__(cls)
    return cls._instance
  
  def __init__(self: AppType, config: Optional[AutoBootConfig] = AutoBootConfig()) -> None:
    if AutoBoot._init_flag is True:
      return
    self.config = config
    self._app_plugins: List[AppPlugin] = []
    self._components: List[Tuple[str, Any]] = []
    AutoBoot.logger: loguru.Logger = None
    AutoBoot._config_data = dict[str, Any]
    AutoBoot._contexts: dict[str, Any] = {}
    AutoBoot._init_flag = True
    
  @classmethod
  def instance(cls: AppType) -> AppType:
    return cls._instance
  
  @staticmethod
  def get_config_data() -> dict[str, Any]:
    return AutoBoot._config_data
  
  @staticmethod
  def get_context(name: str):
    return AutoBoot._contexts.get(name)
    
  
  @property
  def app_plugins(self) -> List[AppPlugin]:
    return self._app_plugins
  
  @app_plugins.setter
  def app_plugins(self, app_plugins: List[AppPlugin]) -> None:
    for ap in app_plugins:
      self.apply(ap)
  
  @property
  def components(self) -> List[Tuple[str, Any]]:
    return self._components
    
  def apply(self: AppType, app_plugin: AppPlugin) -> AppType:
    runner = app_plugin.install()
    AutoBoot._contexts[runner[0]] = runner[1]
    self._app_plugins.append(app_plugin)
  
  def run(self: AppType, expose: Callable[..., R] = None):
    # config environment variables
    env_name = get_env_name()
    
    # load .env
    load_env_file(self.config.config_dir, env_name)
    
    # load yml
    AutoBoot._config_data = load_yaml_file(self.config.config_dir, self.config.yml_config)
    
    # config logger
    from autoboot.application_properties import ApplicationProperties
    AutoBoot.logger = Logging(
      app_name=ApplicationProperties.app_name(),
      module=ApplicationProperties.module(),
      log_dir=ApplicationProperties.log_dir(),
      max_size=ApplicationProperties.log_max_size(),
      retention=ApplicationProperties.log_retention(),
      env_name=env_name
    ).logger
    
    AutoBoot.logger.info(f"application finish load env: {env_name}")
    
    for app_plugin in self._app_plugins:
      app_plugin.env_prepared()

    for app_plugin in self._app_plugins:
      app_plugin.app_started()
      
    AutoBoot.logger.info("application started!")
    
    if expose:
      return expose()