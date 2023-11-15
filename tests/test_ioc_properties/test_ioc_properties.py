
from autoboot import ApplicationProperties, AutoBoot, AutoBootConfig


def testProperties():
  autoboot = AutoBoot(config=AutoBootConfig(config_dir="./tests/test_ioc_properties"))
  autoboot.run()
  
  assert(ApplicationProperties.app_name() == "test-app-dev")