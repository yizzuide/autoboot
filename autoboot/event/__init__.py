import atexit as _atexit

from .event_emitter import Event, EventEmitter
from .application_listener import ApplicationListener
from .component_listener import ComponentListener

__all__ = ["Event", "ApplicationListener", "ComponentListener"]

emitter = EventEmitter()

# register exit callback
_atexit.register(emitter.clear)