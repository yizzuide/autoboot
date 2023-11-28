
import os
from dotenv import dotenv_values

def load_env_file(dir: str, env_name: str):
  """load env file with input opt arg: -e <name>"""
  
  _load_env_file(f"{dir}/.env")
  if env_name:
    _load_env_file(f"{dir}/.env.{env_name}")

def _load_env_file(filepath: str):
  env_kvs = dotenv_values(filepath)
  for k, v in env_kvs.items():
    os.environ[k] = v
      


