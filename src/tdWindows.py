from tdInterface import *
from tdObject import *

import uiautomation as auto


class tdWindows(td):
    @staticmethod
    def getIndicateRectangle() -> Rectangle:
        control=auto.ControlFromCursor()
        rect=control.BoundingRectangle
        return Rectangle(rect.left,rect.top,rect.right,rect.bottom)