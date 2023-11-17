from autoboot.event import EventEmitter, Event

def test_event_emitter():
  emitter = EventEmitter()
  
  @emitter.on("action_paid")
  def receiver(event: Event[str]):
    assert(event.data == "pay order: 1001")
    
  emitter.emit("action_paid", Event("", "pay order: 1001"))