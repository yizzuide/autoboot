
from autoboot import AutoBoot, AutoBootConfig
from autoboot.thread import ThreadPoolTask


def setup_module():
  autoboot = AutoBoot(config=AutoBootConfig(config_dir="./tests/test_ioc_properties"))
  autoboot.run()

def run():
  AutoBoot.logger.info("task run...")

def test_thread_pool():
  task1 = ThreadPoolTask()
  task2 = ThreadPoolTask()
  assert id(task1) == id(task2)
  task1.submit(run)