from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget

from src.GUI.actions import menu
from src.coders import abstractCoder
from src.logger import log


class MainWindow(QMainWindow):
    coder: abstractCoder.Coder = None
    firstCoder: abstractCoder.Coder = None
    secondCoder: abstractCoder.Coder = None

    newCoderWindow: QWidget = None
    testCoderWindow: QWidget = None

    def __init__(self):
        log.debug("Создание главного окна")
        super().__init__()
        self.setFixedSize(250, 34)
        self.setWindowTitle('MAVR')
        self.setWindowIcon(QIcon('Resources/img/pic.png'))

        menu.SetMainToolBar(self)

        self.show()

    def SetCoder(self, coder: abstractCoder.Coder):
        self.coder = coder

    def closeEvent(self, *args, **kwargs):
        if self.newCoderWindow is not None: del self.newCoderWindow
        if self.testCoderWindow is not None: del self.testCoderWindow