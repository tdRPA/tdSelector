from abc import ABC, abstractmethod

from tdObject import *


class td(ABC):
    @staticmethod
    @abstractmethod
    def getIndicateRectangle() -> Rectangle:
        pass