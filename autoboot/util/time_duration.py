
import re
from tzlocal import get_localzone
from whenever import Instant, days, hours, minutes, seconds

def parse(duration_expr: str):
  """Parse a duration expression and return an ZoneDateTime object representing the end time."""
  
  pattern = r'(\d+)([smhd])'
  matches = re.findall(pattern, duration_expr.lower())
  
  dt = Instant.now().to_tz(get_localzone().key)
  for value, unit in matches:
    value = int(value)
    if unit == 's':
      dt += seconds(value)
    elif unit == 'm':
      dt += minutes(value)
    elif unit == 'h':
      dt += hours(value)
    elif unit == 'd':
      dt += days(value)
    else:
      raise ValueError("Unsupported duration format")
  return dt