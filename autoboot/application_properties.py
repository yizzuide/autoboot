
from autoboot.annotation.env import value_component


class ApplicationProperties:
  
  @value_component("autoboot.application.name")
  @staticmethod
  def app_name() -> str:
    return "app"

  @value_component("autoboot.application.module")
  @staticmethod
  def module() -> str:
    return "api"
  
  @value_component("autoboot.application.log.dir")
  @staticmethod
  def log_dir() -> str:
    return "logs"
  
  @value_component("autoboot.application.log.max_size")
  @staticmethod
  def log_max_size() -> str:
    return "100 MB"

  @value_component("autoboot.application.log.retention")
  @staticmethod
  def log_retention() -> str:
    return "30 days"