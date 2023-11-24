from dataclasses import dataclass
from autoboot.event import emitter, Event
from loguru import logger

@dataclass
class PayOrder:
  no: str
  
@dataclass
class RepayOrder:
  no: str
  

def test_event_emitter():
  # send event name action
  emitter.emit(action="pay_action", event=Event("pay order: 1001"))
  # send event with with generic type
  emitter.emit(event=Event(PayOrder("1001")))
  
@emitter.on("pay_action")
def received_payment(event: Event[str]):
  logger.info("received_payment")
  assert(event.data == "pay order: 1001")
  
@emitter.on_event
def received_pay(event: Event[PayOrder]):
  logger.info("received_pay")
  assert(event.data == PayOrder("1001"))

@emitter.on_event
def received_repay(event: Event[RepayOrder]):
  logger.info("received_repay")
  assert(event.data == RepayOrder("1001"))