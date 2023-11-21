from autoboot import AutoBoot, AutoBootConfig
from autoboot.annotation import log_catch


def setup_module():
  autoboot = AutoBoot(config=AutoBootConfig(config_dir="./tests/test_ioc_properties"))
  autoboot.run()

@log_catch("login")
def test_login_catch_log():
  # for test catch log
  #raise Exception("login fail")
  pass
