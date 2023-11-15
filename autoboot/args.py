
import sys
import getopt
from enum import Enum


class Env(Enum):
  DEV = "dev"
  TEST = "test"
  PROD = "prod"
  

def get_env_name() -> str:
  # "e:"中的`:`则表示-e参数后面应该带一个值
  opts, args = getopt.getopt(sys.argv[1:], "e:")
  for op, value in opts:
    if op == "-e":
      return value
  return Env.DEV.value