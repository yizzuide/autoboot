
import os
import json
import yaml
from typing import Any, IO
from durations import Duration
from autoboot.util.capacity import Capacity


class Loader(yaml.SafeLoader):
  """YAML Loader for custom constructor."""

  def __init__(self, stream: IO) -> None:
    """Initialise Loader."""

    try:
      self._root = os.path.split(stream.name)[0]
    except AttributeError:
      self._root = os.path.curdir

    super().__init__(stream)


def construct_include(loader: Loader, node: yaml.Node) -> Any:
  """Include file referenced at node."""

  filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
  extension = os.path.splitext(filename)[1].lstrip(".")

  with open(filename, "r") as f:
    if extension in ("yaml", "yml"):
      return yaml.load(f, Loader)
    elif extension in ("json",):
      return json.load(f)
    else:
      return "".join(f.readlines())


def environment_vars_constructor(loader: Loader, node: yaml.Node) -> Any:
  value = loader.construct_scalar(node)
  if '$' in value:
    # support search env var as $VAR or ${VAR}
    return os.path.expandvars(value)
  return os.getenv(value)


def duration_constructor(loader: Loader, node: yaml.Node) -> Any:
  value = loader.construct_scalar(node)
  return int(Duration(value).to_miliseconds())

def capacity_constructor(loader: Loader, node: yaml.Node) -> Any:
  value = loader.construct_scalar(node)
  return int(Capacity(value).to_bytes())
