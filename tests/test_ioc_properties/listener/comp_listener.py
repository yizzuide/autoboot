
from typing import Any

from autoboot import AutoBoot
from autoboot.event import ComponentListener
from autoboot.meta import Listener

@Listener
class CompListener(ComponentListener):
  
  def after_instantiation(self, name: str, component: Any):
    AutoBoot.logger.warning(f"{name} was instantiated")
  