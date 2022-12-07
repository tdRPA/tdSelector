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
        return text[:100]
        
    @staticmethod
    def getChildren(element: tdElement) -> List[tdElement]:
        autoElement=element._element
        r=[]
        items=autoElement.GetChildren()
        for item in items:
            r.append(tdElement(item,element._td))
        return r
        
    @staticmethod
    def fillProperties(element: tdElement):
        autoElement=element._element
        properties=element.properties
        
        properties['ControlType']=tdProperty(autoElement.ControlType,autoElement.ControlTypeName.rsplit('Control',1)[0])
        properties['AutomationId']=tdProperty(autoElement.AutomationId)
        properties['ClassName']=tdProperty(autoElement.ClassName)
        properties['Text']=tdProperty(autoElement.Name)
        
        acc=autoElement.GetLegacyIAccessiblePattern()        
        properties['accRole']=tdProperty(acc.Role)
        properties['accState']=tdProperty(acc.State)        
        
        process=ps.Process(autoElement.ProcessId)
        properties['PID']=tdProperty(str(process.pid))
        properties['App']=tdProperty(process.name())
        properties['AppPath']=tdProperty(process.exe())

        properties['Framework']=tdProperty(autoElement.FrameworkId)
        properties['HWND']=tdProperty(hex(autoElement.NativeWindowHandle))
        properties['Bounding']=tdProperty(str(autoElement.BoundingRectangle))