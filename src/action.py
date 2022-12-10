from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTreeWidgetItem,QTableWidgetItem,QMenu,QAction,QListWidgetItem
from PySide2.QtGui import QCursor


ui=None

def onRootLoad(rootElement):
    tree=ui.treeElement
    tree.clear()
    
    rootNode=QTreeWidgetItem(tree,[rootElement.display])
    rootNode.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
    rootNode.setData(1,Qt.DisplayRole,rootElement)
    
    tree.itemExpanded.connect(onExpandItem)
    tree.currentItemChanged.connect(onCurrentItemChanged)
    tree.contextMenuEvent=onContextMenuEvent
        
    tree.setCurrentItem(rootNode)
    tree.expandItem(rootNode)
    
    
def onContextMenuEvent(event):
    tree=ui.treeElement    
    
    actionTarget = QAction('Set as Target Element',tree)
    actionAnchor = QAction('Set as Anchor Element',tree)
    actionTarget.triggered.connect(action__Target)
    actionAnchor.triggered.connect(action__Anchor)
    
    menu = QMenu(tree)
    menu.addAction(actionTarget)
    menu.addAction(actionAnchor)
    menu.popup(QCursor.pos())
    
def action__Target(checked):
    item=ui.treeElement.currentItem()
    element=item.data(1,Qt.DisplayRole)
    
    selector=ui.listSelector
    selector.clear()
    while element.parent!=None:
        listItem=QListWidgetItem(element.filterText)
        listItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
        listItem.setCheckState(Qt.Checked)
        selector.insertItem(0,listItem)
        element=element.parent
    if selector.count()>0:
        selector.item(0).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        selector.item(selector.count()-1).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
    
def action__Anchor(checked):
    item=ui.treeElement.currentItem()
    element=item.data(1,Qt.DisplayRole)

    
def onExpandItem(item):
    element=item.data(1,Qt.DisplayRole)
    children=element.children
    for child in children:
        text=child.display
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
        colProperty=QTableWidgetItem(key)
        table.setItem(i, 0, colProperty)
        colText=QTableWidgetItem(text)
        table.setItem(i, 1, colText)
        colText.setToolTip(text)

        i=i+1