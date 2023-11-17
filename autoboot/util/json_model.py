import json
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def stringify(model: T) -> str:
  return model.json(exclude_none=True, by_alias=True)

def parse(model_class: Type[T], data: str) -> T:
  dict = json.loads(data)
  return model_class(**dict)