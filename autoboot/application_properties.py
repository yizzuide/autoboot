
from autoboot.annotation import static_property


class ApplicationProperties:
  
  @static_property("autoboot.application.name")
  def app_name() -> str:
    return "app"

  @static_property("autoboot.application.module")
  def module() -> str:
    return "api"
  
  @static_property("autoboot.application.scan_listener_packages")
  def scan_listener_packages() -> list[str]:
    pass
  
  @static_property("autoboot.application.log.level")
  def log_level() -> str:
    return "INFO"
  
  @static_property("autoboot.application.log.dir")
  def log_dir() -> str:
    return "logs"
  
  @static_property("autoboot.application.log.max_size")
  def log_max_size() -> str:
    return "100 MB"

  @static_property("autoboot.application.log.retention")
  def log_retention() -> str:
    return "30 days"