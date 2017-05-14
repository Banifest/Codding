import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow

from src.GUI.actions import menu
from src.coders import abstractCoder
from src.logger import log


class MainWindow(QMainWindow):
    coder: abstractCoder.Coder = None
    def __init__(self):
        log.debug("Создание главного окна")
        super().__init__()
        self.setFixedSize(300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('Resources/img/pic.png'))

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(QLabel(""))

        menu.SetMainToolBar(self)
        self.setLayout(self.grid)

        self.show()

    def SetCoder(self, coder: abstractCoder.Coder):
        self.coder = coder

def InitMainWindow():
    App = QApplication(sys.argv)
    # win32 = AddCoderWindow()
    window = MainWindow()

    sys.exit(App.exec_())
