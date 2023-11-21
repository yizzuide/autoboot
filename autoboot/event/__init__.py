import atexit as _atexit

from .event_emitter import Event, EventEmitter

__all__ = ["Event"]

emitter = EventEmitter()

# register exit callback
_atexit.register(emitter.clear)