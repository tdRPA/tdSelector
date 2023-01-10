from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTreeWidgetItem,QTableWidgetItem,QMenu,QAction,QListWidgetItem,QStyledItemDelegate,QComboBox
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
    
    selector=ui.listSelector
    selector.currentItemChanged.connect(onCurrentSelectorChanged)
    
    filter=ui.treeFilter
    itemDelegate=FilterItemDelegate()
    filter.setItemDelegateForColumn(0,itemDelegate)
    filter.setItemDelegateForColumn(1,itemDelegate)
    filter.setColumnWidth(0,150)
    filter.setColumnWidth(1,80)
    
    
class FilterItemDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column()==0:
            return None
        else:
            comboBox = QComboBox(parent)
            comboBox.addItem("Full")
            comboBox.addItem("Regex")
            comboBox.addItem("Regex-i")
            comboBox.setItemData(0, '  full match case sensitive  ', Qt.ToolTipRole)
            comboBox.setItemData(1, '  regex match case sensitive  ', Qt.ToolTipRole)
            comboBox.setItemData(2, '  regex match case insensitive  ', Qt.ToolTipRole)
            return comboBox
        
    
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
        listItem.setData(Qt.DisplayRole,element)
        selector.insertItem(0,listItem)
        element=element.parent
    last=selector.count()-1
    selector.item(0).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
    selector.item(last).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
    selector.setCurrentRow(last)
    
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
        
def onCurrentSelectorChanged(item, previous):
    if item==None: # in case clear
        return

    element=item.data(Qt.DisplayRole)
    
    filter=ui.treeFilter
    filter.clear()
    
    selected=QTreeWidgetItem(filter,['selected'])
    selected.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
    selected.setExpanded(True)
    unSelected=QTreeWidgetItem(filter,['unselected'])
    unSelected.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
    unSelected.setExpanded(True)
    
    for key in element.filterProperties:
        value=element.filterProperties[key]
        text=value.text
        
        selectedNode=QTreeWidgetItem(selected if value.isSelectedDefault else unSelected,[key,'FullMatch',text])
        selectedNode.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsUserCheckable)
        selectedNode.setCheckState(0,Qt.Checked if value.isSelected else Qt.Unchecked)