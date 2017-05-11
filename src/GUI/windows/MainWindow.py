import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow

from src.GUI.actions import menu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('Resources/img/pic.png'))

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel("lol"))

        self.setLayout(grid)
        menu.SetMainToolBar(self)

        """QMessageBox.question(self, 'Message',
                             "Are you sure to quit?", QMessageBox.Yes |
                             QMessageBox.No, QMessageBox.Yes)"""

        self.show()


def InitMainWindow():
    App = QApplication(sys.argv)
    # win32 = AddCoderWindow()
    window = MainWindow()

    sys.exit(App.exec_())
