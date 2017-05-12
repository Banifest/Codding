from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox, QToolBar

from src.GUI.windows import MainWindow
from src.GUI.windows.AddCoderWindow import AddCoderWindow
from src.GUI.windows.TestCoderWindow import TestCoderWindow


def SetMainToolBar(window: MainWindow):
    window.mainToolBar: QToolBar
    window.mainToolBar = window.addToolBar("KitCoders")
    window.mainToolBar.addAction(NewCoderAction(window))
    window.mainToolBar.addAction(TestCoderAction(window))


class MainToolBar(QMainWindow):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.addAction(NewCoderAction(window))


class NewCoderAction(QAction):
    window: MainWindow


    def createWindow(self):
        AddCoderWindow(self.window)

    def __init__(self, window: MainWindow):
        super().__init__(QIcon("Resources/img/AddCoder.png"), "&Добавить кодер", window)
        self.window = window
        self.setShortcut("Ctrl+Shift+A")
        self.triggered.connect(self.createWindow)


class TestCoderAction(QAction):
    window: MainWindow


    def __init__(self, window: MainWindow):
        super().__init__(QIcon("Resources/img/TestCoder.jpg"), "&Протестировать кодер", window)
        self.window = window
        self.setShortcut("Ctrl+Shift+T")

        self.triggered.connect(self.createWindow)

    def createWindow(self):
        if self.window.coder is not None:
            TestCoderWindow(self.window)
        else:
            QMessageBox.warning(self.window, "А кодер кто будет создовать?",
                                "Для начала тестирования нужно создать кодер",
                                QMessageBox.Ok)
