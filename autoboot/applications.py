
import loguru
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, TypeVar
from autoboot.args import get_env_name
from autoboot.logging import Logging
from autoboot.plugin import AppPlugin
from autoboot.process import load_env_file, load_yaml_file

# define AutoBoot class type
AppType = TypeVar("AppType", bound="AutoBoot")

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
  
  __instance = None
  __init_flag = False
  
  def __new__(cls, config: Optional[AutoBootConfig]) -> AppType:
    # create instance only once
    if cls.__instance is None:
        cls.__instance = super().__new__(cls)
    return cls.__instance
  
  def __init__(self: AppType, config: Optional[AutoBootConfig] = AutoBootConfig()) -> None:
    if AutoBoot.__init_flag is True:
      return
    self.config = config
    AutoBoot.logger: loguru.Logger = None
    self.__app_plugins: List[AppPlugin] = []
    self.__components: List[Tuple[str, Any]] = []
    AutoBoot.__config_data = dict[str, Any]
    AutoBoot.__init_flag = True
    
  @classmethod
  def instance(cls: AppType) -> AppType:
    return cls.__instance
  
  @staticmethod
  def get_config_data() -> dict[str, Any]:
    return AutoBoot.__config_data
    
  
  @property
  def app_plugins(self) -> List[AppPlugin]:
    return self.__app_plugins
  
  @app_plugins.setter
  def app_plugins(self, app_plugins: List[AppPlugin]) -> None:
    self.__app_plugins = app_plugins 
  
  @property
  def components(self) -> List[Tuple[str, Any]]:
    return self.__components
    
  def apply(self: AppType, app_plugin: AppPlugin) -> None:
    app_plugin.install(self)
    self.__app_plugins.append(app_plugin)
  
  def run(self: AppType):
    # config environment variables
    env_name = get_env_name()
    
    # load .env
    load_env_file(self.config.config_dir, env_name)
    
    # load yml
    AutoBoot.__config_data = load_yaml_file(self.config.config_dir, self.config.yml_config)
    
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
    
    for app_plugin in self.__app_plugins:
      app_plugin.env_prepared()

    for app_plugin in self.__app_plugins:
      app_plugin.app_started()
      
    AutoBoot.logger.info("application started!")