
import os
from typing import Any

import yaml
from .yaml_constructors import Loader
from autoboot.util.object_navigator import get_value_by


def load_yaml_file(dir: str, file_name: str) -> dict[str, Any]:
  file_path: str
  if os.path.exists(os.path.join(dir, file_name + ".yml")):
    file_path = f"{file_name}.yml"
  else:
    file_path = f"{file_name}.yaml"
  with open(os.path.join(dir, file_path), 'r') as f:
    return yaml.load(f, Loader)
  
def get_yml_value(config_data: dict[str, Any], keypath: str) -> Any:
  value = get_value_by(config_data, keypath)
  if not value:
    return None
  if isinstance(value, str) and value.startswith("env(") and value.endswith(")"):
    return os.getenv(value[4:-1])
  return value
