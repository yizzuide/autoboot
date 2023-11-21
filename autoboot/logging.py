from __future__ import annotations  # Postponed Evaluation of Annotations (PEP 563) was unusable, it requires a __future__ import.

import os
import sys
import loguru
from typing import TypeVar
from autoboot.args import Env
from loguru import logger

LoggingType = TypeVar("LoggingType", bound="Logging")

class Logging:
  """
  Logging class wrapper with loguru.
  """
  
  _instance: LoggingType = None
  
  def __init__(self, log_dir: str, app_name: str, module: str, max_size: str, retention: str, env_name: str):
    self.log_dir = log_dir
    self.app_name = app_name
    self.module = module
    self.max_size = max_size
    self.retention = retention
    self.logger = self.console_logger() if env_name == Env.DEV.value else self.file_rotation_logger()
    Logging._instance = self
    
  def console_logger(self) -> loguru.Logger:
    logger.configure(
      handlers=[{
        "sink": sys.stdout,
        "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        "level": "DEBUG",
        "colorize": True,
        "backtrace": True,
      }])
    return logger
    
  def file_rotation_logger(self) -> loguru.Logger:
    log_app_dir = os.path.join(self.log_dir, self.app_name)
    if not os.path.exists(log_app_dir):
      os.makedirs(log_app_dir)
    logger.configure(
      handlers=[{
        "sink": f"{log_app_dir}/{self.module}-{{time:YYYY-MM-DD}}.log",
        "rotation": self.max_size,
        "retention": self.retention,
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{module}:{function}:{line} - {message}",
        "colorize": False,
        "enqueue": True,
        "backtrace": True,
      }])
    return logger
  
  @classmethod
  def catch_file_rotation_logger(cls, user_case: str):
    log_app_dir = os.path.join(cls._instance.log_dir, cls._instance.app_name)
    if not os.path.exists(log_app_dir):
      os.makedirs(log_app_dir)
    logger.configure(extra={"user_case": user_case})
    logger.add(
      f"{log_app_dir}/{cls._instance.module}-error-{{time:YYYY-MM-DD}}.log",
      rotation=cls._instance.max_size,
      retention=cls._instance.retention,
      level="ERROR",
      format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{module}:{function}:{line} -> [{extra[user_case]}] - {message}",
      catch=True,
      enqueue=True,
      backtrace=True
    )
      


