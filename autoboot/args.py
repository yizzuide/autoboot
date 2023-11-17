import os
import sys
import getopt
import argparse
from enum import Enum


class Env(Enum):
  DEV = "dev"
  TEST = "test"
  PROD = "prod"
  

def get_env_name() -> str:
  parser = argparse.ArgumentParser(description="Startup")
  parser.add_argument("-e", required=False, dest="env_name", help="env name")
  args = parser.parse_known_args()
  if args[0].env_name:
    return args[0].env_name
  else:
    env_name = os.getenv("ENV_NAME")
    return env_name if env_name else Env.DEV.value
    
  # ops = sys.argv[1:]
  # if "-e" in ops:
  #   opts, args = getopt.getopt(ops, "e:") # "e:"中的`:`则表示-e参数后面应该带一个值
  #   for op, value in opts:
  #     if op == "-e":
  #       return value
  # return Env.DEV.value