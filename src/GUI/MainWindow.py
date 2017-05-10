import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('lol.png'))
        self.show()


def InitMainWindow():
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec_())
