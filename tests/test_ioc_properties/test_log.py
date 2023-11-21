from loguru import logger
from autoboot import AutoBoot, AutoBootConfig
from autoboot.logging import Logging


def setup_module():
  autoboot = AutoBoot(config=AutoBootConfig(config_dir="./tests/test_ioc_properties"))
  autoboot.run()
  Logging.catch_file_rotation_logger("login")
  

@logger.catch
def test_login_catch_log():
  # for test catch log
  #raise Exception("login fail")
  pass
