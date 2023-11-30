
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ApplicationListener(Protocol):
  """Global application listener protocol."""
  
  def on_env_prepared(self, config: dict[str, Any]):...
  
  def on_started(self):...