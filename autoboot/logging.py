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
  
  __instance: LoggingType = None
  
  def __init__(self, log_dir, app_name, module, max_size, retention, env_name):
    self.log_dir = log_dir
    self.app_name = app_name
    self.module = module
    self.max_size = max_size
    self.retention = retention
    self.logger = self.console_logger() if env_name == Env.DEV.value else self.file_rotation_logger()
    Logging.__instance = self.logger
    
  def console_logger(self) -> loguru.Logger:
    logger.configure(
      handlers=[{
        "sink": sys.stdout,
        "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        "level": "DEBUG",
        "colorize": True,
        "backtrace": True,
        "dialog": True,
      }])
    return logger
    
  def file_rotation_logger(self) -> loguru.Logger:
    log_app_dir = os.path.join(self.log_dir, self.app_name)
    os.makedirs(log_app_dir, exist_ok=True)
    logger.configure(
      handlers=[{
        "sink": f"{log_app_dir}/{self.app_name}_{self.module}-{{time:YYYY-MM-DD}}.log",
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[module_name]}:{name}:{module}:{function}:{line} - {message}",
        "level": "INFO",
        "colorize": False,
        "enqueue": True,
        "backtrace": True,
        "dialog": True,
      }])
    return logger
  
  @staticmethod
  def catch_file_rotation_logger(user_case):
    log_app_dir = os.path.join(Logging.__instance.log_dir, Logging.__instance.app_name)
    os.makedirs(log_app_dir, exist_ok=True)
    logger.bind(user_case=user_case)
    logger.add(
      f"{log_app_dir}/{Logging.__instance.app_name}_{Logging.__instance.module}-error-{{time:YYYY-MM-DD}}.log",
      rotation=f"{Logging.__instance.max_size}MB",
      retention=Logging.__instance.retention,
      level="ERROR",
      format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{module}:{function}:{line} - {extra[user_case]} - {message}",
      enqueue=True,
      backtrace=True
    )
      


