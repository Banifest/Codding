import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from src.GUI.actions import menu
from src.coders import abstractCoder
from src.logger import log


class MainWindow(QMainWindow):
    coder: abstractCoder.Coder = None
    firstCoder: abstractCoder.Coder = None
    secondCoder: abstractCoder.Coder = None


    def __init__(self):
        log.debug("Создание главного окна")
        super().__init__()
        self.setFixedSize(300, 30)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('Resources/img/pic.png'))

        menu.SetMainToolBar(self)

        self.show()

    def SetCoder(self, coder: abstractCoder.Coder):
        self.coder = coder

def InitMainWindow():
    App = QApplication(sys.argv)
    # win32 = AddCoderWindow()

    window = MainWindow()

    sys.exit(App.exec_())
