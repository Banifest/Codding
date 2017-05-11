from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel, QWidget


class AddCoderWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        parent.newWindow = self
        self.setWindowIcon(QIcon("Resources/img/AddCoder.png"))
        self.setWindowTitle("Добавить кодер")
        self.setGeometry(400, 400, 200, 200)

        self.comboBox: QComboBox = QComboBox()
        self.comboBox.addItem("Рида-Соломона")
        self.comboBox.addItem("Циклический")
        self.comboBox.addItem("Свёрточный")
        self.comboBox.addItem("Фонтанный")
        self.myLabel: QLabel = QLabel("NoChange")

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.comboBox)
        grid.addWidget(self.myLabel)
        self.setLayout(grid)

        self.comboBox.activated[str].connect(self.lol)

        self.show()

    def lol(self, text: str):
        print(text)
