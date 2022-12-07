from abc import ABC, abstractmethod

from tdObject import *

from typing import List


class td(ABC):
    @staticmethod
    @abstractmethod
    def getIndicateRectangle() -> Rectangle:
        pass
        
    @staticmethod
    @abstractmethod
    def getRootElement() -> tdElement:
        pass
        
    @staticmethod
    @abstractmethod
    def getText(element: tdElement,withPrefix=True) -> str:
        pass
        
    @staticmethod
    @abstractmethod
    def getChildren(element: tdElement) -> List[tdElement]:
        pass
        
    @staticmethod
    @abstractmethod
    def fillProperties(element: tdElement):
        pass
        
