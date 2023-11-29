
import re

class Capacity(object):
  """Capacity represent resolver."""
  
  pattern = r'^(\d+)([KMGT])B$'
  
  def __init__(self, representation: str) -> None:
    parts = re.match(Capacity.pattern, representation)
    if parts is None:
      raise ValueError(f'Invalid capacity representation: {representation}')
    self.value = int(parts[1])
    self.unit = parts[2]
    
  def __str__(self) -> str:
    return f'{self.value}{self.unit}'
  
  def __repr__(self) -> str:
    return f'Capacity({self.value}, {self.unit})'
  
  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Capacity):
      return False
    return self.value == other.value and self.unit == other.unit
  
  def to_bytes(self) -> int:
    """
    Converts capacity to bytes.
    """
    
    if self.unit == 'K':
      return self.value * 1024
    elif self.unit == 'M':
      return self.value * 1024 * 1024
    elif self.unit == 'G':
      return self.value * 1024 * 1024 * 1024
    elif self.unit == 'T':
      return self.value * 1024 * 1024 * 1024 * 1024 
    else:
      raise ValueError(f'Invalid capacity unit: {self.unit}')
    
  def to_kb(self) -> int:
    """
    Converts capacity to KiB.
    """
    
    if self.unit == 'K':
      return self.value
    elif self.unit == 'M':
      return self.value * 1024
    elif self.unit == 'G':
      return self.value * 1024 * 1024
    elif self.unit == 'T':
      return self.value * 1024 * 1024 * 1024
    else:
      raise ValueError(f'Invalid capacity unit: {self.unit}')
      
  def to_mb(self) -> float:
    """
    Converts capacity to MiB.
    """
    
    if self.unit == 'K':
      return self.value / 1024.0
    elif self.unit == 'M':
      return self.value
    elif self.unit == 'G':
      return self.value * 1024
    elif self.unit == 'T':
      return self.value * 1024 * 1024
    else:
      raise ValueError(f'Invalid capacity unit: {self.unit}')
  
  def to_gb(self) -> float:
    """
    Converts capacity to GiB.
    """
    
    if self.unit == 'K':
      return self.value / 1024.0 / 1024
    elif self.unit == 'M':
      return self.value / 1024.0
    elif self.unit == 'G':
      return self.value
    elif self.unit == 'T':
      return self.value * 1024
    else:
      raise ValueError(f'Invalid capacity unit: {self.unit}')
    
  def to_tb(self) -> float:
    """
    Converts capacity to TiB.
    """
    
    if self.unit == 'K':
      return self.value / 1024.0 / 1024 / 1024
    elif self.unit == 'M':
      return self.value / 1024.0 / 1024
    elif self.unit == 'G':
      return self.value / 1024.0
    elif self.unit == 'T':
      return self.value
    else:
      raise ValueError(f'Invalid capacity unit: {self.unit}')
  
  