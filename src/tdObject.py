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
    def __init__(self,value,text=None,isFilter=False,isSelectedDefault=False):
        self.value=value
        if text==None:
            self.text=str(value)
        else:
            self.text='%s(%s)' % (str(value),str(text))
        self.isFilter=isFilter
        self.isSelectedDefault=isSelectedDefault
        self.isSelected=isSelectedDefault
        
        
class tdElement():
    def __init__(self,element,td):
        self._element=element
        self._td=td
        
        self.properties=OrderedDict()
        self._filterProperties=None
        td.fillProperties(self)
        
    @property
    def display(self):
        return self._td.getText(self,withPrefix=True)
        
    @property
    def text(self):
        return self._td.getText(self)
        
    @property
    def parent(self):
        return self._td.getParent(self)
        
    @property    
    def children(self):
        return self._td.getChildren(self)
        
    @property
    def filterText(self):
        text='{ '
        tag=False
        for key in self.properties:
            property=self.properties[key]
            if property.isFilter and property.isSelected:
                text+='"%s" : "%s" , ' %(key,str(property.value))
                tag=True
        if tag:
            text=text[:-3]
        text+=' }'
        return text
        
    @property
    def filterProperties(self):
        if self._filterProperties==None:
            filters=OrderedDict()
            for key in self.properties:
                value=self.properties[key]
                if value.isFilter:
                    filters[key]=value
            self._filterProperties=filters
        
        return self._filterProperties