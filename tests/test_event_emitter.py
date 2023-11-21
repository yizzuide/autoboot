from autoboot.event import emitter, Event
from loguru import logger

def test_event_emitter():
  emitter.emit("action_paid", Event("", "pay order: 1001"))
  
@emitter.on("action_paid")
def receiver(event: Event[str]):
  logger.info("received action paid")
  assert(event.data == "pay order: 1001")