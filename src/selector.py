import sys

from PySide2 import QtCore
from PySide2.QtCore import Qt,QTimer
from PySide2.QtWidgets import QApplication,QMainWindow,QWidget
from PySide2.QtGui import QPainter,QPen,QColor

from layout import Ui_MainWindow

from tdObject import *
from tdWindows import tdWindows as td

import keyboard

import action


class Highlighter(QWidget):
    def __init__(self,callBackFinished,callBackCanceled):
        super().__init__()
        self.setWindowFlag(Qt.SubWindow)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.area=None
        self.isFinished=False
        self.isCanceled=False
        self.timerId=None

        self.callBackFinished=callBackFinished
        self.callBackCanceled=callBackCanceled

    def onFinished(self):
        self.isFinished=True

    def onCanceled(self):
        self.isCanceled=True

    def paintEvent(self, event):
        if self.area!=None:
            painter = QPainter(self)
            #painter.fillRect(0, 0, self.area.width, self.area.height,QColor(135,206,235, 100))
            painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
            painter.drawRect(0, 0, self.area.width, self.area.height)
            
    def timerEvent(self, event):
        if self.isFinished:
            self.stop()
            self.callBackFinished()
        elif self.isCanceled:
            self.stop()
            self.callBackCanceled()
        else:
            self.refresh()
        
    def refresh(self):
        self.hide()
        self.area=td.getIndicateRectangle()
        self.setGeometry(self.area.left, self.area.top, self.area.width, self.area.height)
        self.show()
        
    def start(self):
        self.area=None
        self.isFinished=False
        self.isCanceled=False
        self.timerId=self.startTimer(100)
        keyboard.add_hotkey('ctrl',self.onFinished)
        keyboard.add_hotkey('esc',self.onCanceled)
        
    def stop(self):
        self.killTimer(self.timerId)
        keyboard.clear_all_hotkeys()

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        self.setupActions()
        
        self.highlighter=Highlighter(self.highlightFinished,self.highlightCanceled)
        
        action.ui=self.ui
        self.rootElement=td.getRootElement()
        action.onRootLoad(self.rootElement)
        
    def setupActions(self):
        self.ui.actionIndicate_Element.triggered.connect(self.action__Indicate_Element)

    def highlightFinished(self):
        self.highlighter.hide()
        self.show()

    def highlightCanceled(self):
        self.highlighter.hide()
        self.show()

    def action__Indicate_Element(self,checked):
        self.hide()
        self.highlighter.start()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    
    #setup i18n
    trans=QtCore.QTranslator()
    isLoaded=trans.load('default','i18n')
    if isLoaded:
        print('language_country: default.qm')
        app.installTranslator(trans)
    else:
        local=QtCore.QLocale()
        language_country=local.name()
        print('language_country: ', language_country)
        isLoaded=trans.load(language_country,'i18n')
        if isLoaded:
            app.installTranslator(trans)
        else:
            language=language_country.split('_')[0]
            trans.load(language,'i18n')
            app.installTranslator(trans)
    
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())