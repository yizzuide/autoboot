

from typing import Type

from autoboot import AutoBoot
from autoboot.event import ApplicationListener, ComponentListener


def Listener(cls):
  
  if issubclass(cls, ApplicationListener):
      AutoBoot.instance().addListener(Type.__new__(cls))
  elif issubclass(cls, ComponentListener):
    AutoBoot.instance().addComponentListener(Type.__new__(cls))