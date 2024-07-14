
from autoboot import ApplicationProperties, AutoBoot, AutoBootConfig
from autoboot.annotation import component, conditional


@conditional(value="service.hello.enable", having_value=True)
@component()
class HelloService(object):
  def __init__(self) -> None:
    self.list = []
      
  def add(self, item):
    self.list.append(item)
    
  def getItems(self):
    return self.list


def testProperties():
  autoboot = AutoBoot(config=AutoBootConfig(config_dir="./tests/test_ioc_properties"))
  autoboot.run()
    
  assert(ApplicationProperties.app_name() == "app-dev")
  assert(ApplicationProperties.log_level() == "DEBUG")
  assert(id(HelloService()) == id(HelloService()))