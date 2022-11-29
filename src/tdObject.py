

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