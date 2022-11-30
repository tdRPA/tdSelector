from tdInterface import *
from tdObject import *

import uiautomation as auto
import psutil as ps

import re


class tdWindows(td):
    @staticmethod
    def getIndicateRectangle() -> Rectangle:
        control=auto.ControlFromCursor()
        rect=control.BoundingRectangle
        return Rectangle(rect.left,rect.top,rect.right,rect.bottom)
        
    @staticmethod
    def getRootElement() -> tdElement:
        root=auto.GetRootControl()
        return tdElement(root,tdWindows)
        
    @staticmethod
    def getProcessId(element: tdElement) -> int:
        autoElement=element._element
        return autoElement.ProcessId
        
    @staticmethod
    def getText(element: tdElement) -> str:
        autoElement=element._element
        if autoElement.GetParentControl()==None:
            text=autoElement.Name
        elif autoElement.GetParentControl().GetParentControl()==None:
            process=ps.Process(autoElement.ProcessId)
            text=process.name()+' '+autoElement.Name
        else:
            text=autoElement.ControlTypeName.rsplit('Control',1)[0]+' '+autoElement.Name
        text=re.sub(r'\s+',' ',text)
        return text[:50]
        
    @staticmethod
    def getChildren(element: tdElement) -> List[tdElement]:
        autoElement=element._element
        r=[]
        items=autoElement.GetChildren()
        for item in items:
            r.append(tdElement(item,element._td))
        return r
        
