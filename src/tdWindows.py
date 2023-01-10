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
    def getText(element: tdElement,withPrefix=False) -> str:
        autoElement=element._element
        text=re.sub(r'\s+',' ',autoElement.Name)[:100]
        if withPrefix:
            if autoElement.GetParentControl()==None:
                prefix=''
            elif autoElement.GetParentControl().GetParentControl()==None:
                process=ps.Process(autoElement.ProcessId)
                prefix=process.name()
            else:
                prefix=autoElement.ControlTypeName.rsplit('Control',1)[0]
            text=prefix+' '+text
        
        return text.strip()
        
    @staticmethod
    def getParent(element: tdElement) -> tdElement:
        autoElement=element._element
        autoParent=autoElement.GetParentControl()
        if autoParent!=None:
            return tdElement(autoParent,element._td)
        else:
            return None
        
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
        
        properties['ControlType']=tdProperty(autoElement.ControlType,autoElement.ControlTypeName.rsplit('Control',1)[0], isFilter=True)
        properties['AutomationId']=tdProperty(autoElement.AutomationId, isFilter=True)
        properties['ClassName']=tdProperty(autoElement.ClassName, isFilter=True)
        properties['Text']=tdProperty(element.text, isFilter=True)
        
        acc=autoElement.GetLegacyIAccessiblePattern()        
        properties['aaRole']=tdProperty(acc.Role, isFilter=True)
        properties['aaState']=tdProperty(acc.State, isFilter=True)        
        
        process=ps.Process(autoElement.ProcessId)
        properties['PID']=tdProperty(str(process.pid))
        properties['App']=tdProperty(process.name())
        properties['AppPath']=tdProperty(process.exe())

        properties['Framework']=tdProperty(autoElement.FrameworkId)
        properties['HWND']=tdProperty(hex(autoElement.NativeWindowHandle))
        properties['Bounding']=tdProperty(str(autoElement.BoundingRectangle))
        
        #set properties "isSelectedDefault"
        if not (properties['Text'].value in [None,'']):
            properties['Text'].isSelectedDefault=True
            properties['Text'].isSelected=True
        if not (properties['AutomationId'].value in [None,'']):
            properties['AutomationId'].isSelectedDefault=True
            properties['AutomationId'].isSelected=True
        elif not (properties['aaRole'].value in [None,'']):
            properties['aaRole'].isSelectedDefault=True
            properties['aaRole'].isSelected=True
        elif not (properties['ClassName'].value in [None,'']):
            properties['ClassName'].isSelectedDefault=True
            properties['ClassName'].isSelected=True
        elif not (properties['ControlType'].value in [None,'']):
            properties['ControlType'].isSelectedDefault=True
            properties['ControlType'].isSelected=True