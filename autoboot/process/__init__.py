import yaml
import re
from autoboot.util.capacity import Capacity
from .env_process import load_env_file
from .yaml_parser import load_yaml_file, get_yml_value
from .yaml_constructors import (
  Loader, 
  construct_include, 
  environment_vars_constructor, 
  duration_constructor,
  capacity_constructor
)


yaml.add_constructor(u'!include', construct_include, Loader)
yaml.add_constructor(u'!env', environment_vars_constructor, Loader)
yaml.add_constructor(u'!ts', duration_constructor, Loader)
yaml.add_constructor(u'!cap', capacity_constructor, Loader)

pattern = re.compile(r'^(\d+h)?\s*(\d+m)?\s*(\d+s)?\s*(\d+ms)?\s*$')
yaml.add_implicit_resolver(u'!ts', pattern, Loader=Loader)
yaml.add_implicit_resolver(u'!cap', re.compile(pattern=Capacity.pattern), Loader=Loader)

__all__ = ["load_env_file", "load_yaml_file", "get_yml_value"]
