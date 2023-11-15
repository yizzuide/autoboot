
from __future__ import annotations  # Postponed Evaluation of Annotations (PEP 563) was unusable, it requires a __future__ import.

import os

import loguru
from autoboot.args import Env
from loguru import logger


class Logging:
  """
  Logging class wrapper with loguru.
  """
  def __init__(self, log_dir, app_name, module, max_size, retention, env_name):
    self.log_dir = log_dir
    self.app_name = app_name
    self.module = module
    self.max_size = max_size
    self.retention = retention
    self.logger = self.console_logger() if env_name == Env.DEV.value else self.file_rotation_logger()
    
  def console_logger(self) -> loguru.Logger:
    logger.add(
      "console.log",
      format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
      level="DEBUG",
      colorize=True,
      backtrace=True,
      diagnose=True
    )
    return logger
    
  def file_rotation_logger(self) -> loguru.Logger:
    log_app_dir = os.path.join(self.log_dir, self.app_name)
    os.makedirs(log_app_dir, exist_ok=True)
    logger.add(
      f"{log_app_dir}/{self.app_name}_{self.module}-{{time:YYYY-MM-DD}}.log",
      rotation=f"{self.max_size}MB",
      retention=self.retention,
      level="INFO",
      format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
      enqueue=True,
      backtrace=True
    )
    return logger
      


