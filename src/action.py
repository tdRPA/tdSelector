from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTreeWidgetItem,QTableWidgetItem

import re


ui=None

def onRootLoad(rootElement):
    tree=ui.treeElement
    tree.clear()
    
    rootNode=QTreeWidgetItem(tree,[rootElement.text])
    rootNode.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
    rootNode.setData(1,Qt.DisplayRole,rootElement)
    
    tree.itemExpanded.connect(onExpandItem)
    tree.currentItemChanged.connect(onCurrentItemChanged)
        
    tree.setCurrentItem(rootNode)
    tree.expandItem(rootNode)
    
    
def onExpandItem(item):
    element=item.data(1,Qt.DisplayRole)
    children=element.children
    for child in children:
        text=child.text
        childNode=QTreeWidgetItem(item,[text])
        childNode.setToolTip(0,text)
        if len(child.children)==0:
            childNode.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)
        else:
            childNode.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        childNode.setData(1,Qt.DisplayRole,child)
        

def onCurrentItemChanged(item, previous):
    element=item.data(1,Qt.DisplayRole)
    
    table=ui.tableProperty
    table.clear()

    properties=element.properties
    table.setRowCount(len(properties))
    
    i=0
    for key in element.properties:
        text=properties[key].text
        text=re.sub(r'\s+',' ',text)[:100]
        colProperty=QTableWidgetItem(key)
        table.setItem(i, 0, colProperty)
        colText=QTableWidgetItem(text)
        table.setItem(i, 1, colText)
        colText.setToolTip(text)

        i=i+1