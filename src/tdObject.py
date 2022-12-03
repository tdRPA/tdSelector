from collections import OrderedDict

import psutil as ps


class Rectangle():
    def __init__(self,left,top,right,bottom):
        self.left=left
        self.top=top
        self.right=right
        self.bottom=bottom
        
    @property
    def width(self):
        return self.right-self.left
        
    @property
    def height(self):
        return self.bottom-self.top
        
        
class tdProperty():
    def __init__(self,value,isFilter=False):
        self.value=value
        self.isFilter=isFilter
        
        
class tdElement():
    def __init__(self,element,td):
        self._element=element
        self._td=td
        
        properties=OrderedDict()
        process=ps.Process(self._td.getProcessId(self))
        properties['PID']=tdProperty(str(process.pid))
        properties['App']=tdProperty(process.name())
        properties['AppPath']=tdProperty(process.exe())
        
        self.properties=properties
        
    @property
    def text(self):
        return self._td.getText(self)
        
    @property    
    def children(self):
        return self._td.getChildren(self)