from enum import Enum
from pydantic import BaseModel
from autoboot.util import json_model

def test_parse():
  class Address(BaseModel):
    city: str
    
  class UserType(Enum):
    NORMAL = 0
    VIP = 1
  
  class User(BaseModel):
    name: str
    age: int
    address: Address
    type: UserType
  
  data = '{"name": "John", "age": 30, "type": 0, "address": {"city": "New York"}}'
  user = json_model.parse(User, data)
  assert(user==User(name="John", age=30, type=UserType.NORMAL, address=Address(city="New York")))