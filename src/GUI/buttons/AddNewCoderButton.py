from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QPushButton


class AddNewCoderButton(QPushButton):
    def __init__(self, window: QWindow):
        super().__init__("", window)
