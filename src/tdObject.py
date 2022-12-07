from collections import OrderedDict


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
    def __init__(self,value,text=None,isFilter=False):
        self.value=value
        if text==None:
            self.text=str(value)
        else:
            self.text='%s(%s)' % (str(value),str(text))
        self.isFilter=isFilter
        
        
class tdElement():
    def __init__(self,element,td):
        self._element=element
        self._td=td
        
        self.properties=OrderedDict()
        td.fillProperties(self)
        
    @property
    def text(self):
        return self._td.getText(self)
        
    @property    
    def children(self):
        return self._td.getChildren(self)