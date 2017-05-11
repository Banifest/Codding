from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QToolBar

from src.GUI.windows.AddCoderWindow import AddCoderWindow


def SetMainToolBar(window: QMainWindow):
    window.mainToolBar: QToolBar
    window.mainToolBar = window.addToolBar("KitCoders")
    # window.mainToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    window.mainToolBar.addAction(ActionNewCoder(window))
    # window.mainToolBar.setOrientation(2)


class MainToolBar(QMainWindow):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.addAction(ActionNewCoder(window))



class ActionNewCoder(QAction):
    window: QMainWindow


    def createWindow(self):
        a = AddCoderWindow(self.window)
        pass

    def __init__(self, window: QMainWindow):
        super().__init__(QIcon("Resources/img/AddCoder.png"), '&Добавить кодер', window)
        self.window = window
        self.setShortcut("Ctrl+Shift+A")
        self.triggered.connect(self.createWindow)
        #        self.changed.connect(window.setWindowIcon(QIcon('Resources/img/AddCoder.png')))
        #        self.triggered.connect()
