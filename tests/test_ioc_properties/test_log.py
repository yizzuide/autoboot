from autoboot import ApplicationProperties, AutoBoot, AutoBootConfig
from autoboot.annotation import log_catch
import pytest

def setup():
  autoboot = AutoBoot(config=AutoBootConfig(config_dir="./tests/test_ioc_properties"))
  autoboot.run()

@pytest.fixture
@log_catch("auto")
def test_login_catch_log(setup):
   raise Exception("Login Fail")
