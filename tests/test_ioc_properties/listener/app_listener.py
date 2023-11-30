
from autoboot import AutoBoot
from autoboot.event import ApplicationListener
from autoboot.meta import Listener

@Listener
class AppListener(ApplicationListener):
  
  def on_started(self):
    AutoBoot.logger.warning("Application started")