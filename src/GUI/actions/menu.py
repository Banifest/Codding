from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QToolBar

from Resources.stringConsts import CODER_NAMES
from src.GUI.windows import MainWindow
from src.GUI.windows.AddCoderWindow import AddCoderWindow
from src.GUI.windows.TestCascadeCoderWindow import TestCascadeCoderWindow
from src.GUI.windows.TestCoderWindow import TestCoderWindow
from src.coders import convolutional, cyclical, fountain, linear


def SetMainToolBar(window: MainWindow):
    window.mainToolBar: QToolBar
    window.mainToolBar = window.addToolBar("KitCoders")
    window.mainToolBar.addAction(NewCoderAction(window))
    window.mainToolBar.addAction(TestCoderAction(window))
    window.mainToolBar.addAction(TestCascadeCoderAction(window))
    window.mainToolBar.addAction(AboutCoder(window))


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
        self.window: MainWindow.MainWindow = window
        self.setShortcut("Ctrl+Shift+T")
        self.triggered.connect(self.createWindow)

    def createWindow(self):
        if self.window.coder is not None:
            TestCoderWindow(self.window)
        else:
            QMessageBox.warning(self.window, "А кодер кто будет создовать?",
                                "Для начала тестирования нужно создать кодер",
                                QMessageBox.Ok)


class TestCascadeCoderAction(QAction):
    window: MainWindow

    def __init__(self, window: MainWindow):
        super().__init__(QIcon("Resources/img/TestCascadeCoder.png"), "&Протестировать каскадный кодер", window)
        self.window = window
        self.setShortcut("Ctrl+Shift+С")

        self.triggered.connect(self.createWindow)

    def createWindow(self):
        if self.window.firstCoder is not None and self.window.secondCoder is not None:
            TestCascadeCoderWindow(self.window)
        else:
            QMessageBox.warning(self.window, "А кодеры кто будет создовать?",
                                "Для начала тестирования нужно создать два кодера",
                                QMessageBox.Ok)


class AboutCoder(QAction):
    window: MainWindow

    def __init__(self, window: MainWindow):
        super().__init__(QIcon("Resources/img/InformationCoder.png"), "&Информация о кодере", window)
        self.window = window
        self.setShortcut("Ctrl+Shift+I")

        self.triggered.connect(self.createWindow)

    def createWindow(self):
        if self.window.coder is not None:
            information: str = ""
            if isinstance(self.window.coder, linear.Coder.Coder):
                information = CODER_NAMES[0]
            elif isinstance(self.window.coder, cyclical.Coder.Coder):
                information = CODER_NAMES[1]
            elif isinstance(self.window.coder, convolutional.Coder.Coder):
                information = CODER_NAMES[2]
            elif isinstance(self.window.coder, fountain.LubyTransform.Coder):
                information = CODER_NAMES[3]
            QMessageBox.information(self.window, "Информация о последнем добавленом кодере",
                                    "Кодер типа - {0}\n"
                                    "Избыточность информации - {1}%\n"
                                    "Скорость кодера - {2}\n".format(
                                            information,
                                            self.window.coder.GetRedundancy(),
                                            self.window.coder.GetSpeed()),
                                    QMessageBox.Ok
                                    )
        else:
            QMessageBox.warning(self.window, "А кодер кто будет создовать?",
                                "Для начала нужно создать кодер",
                                QMessageBox.Ok)
