from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from src.GUI.windows import MainWindow
from src.coders import convolutional, cyclical, hemming
from src.coders.fountain import LubyTransform
from src.logger import log


class AddCoderWindow(QWidget):
    windowParent: MainWindow

    grid: QGridLayout
    comboBox: QComboBox
    submitButton: QPushButton

    sizePackageTextBox: QLineEdit
    listPolynomialTextBox: QLineEdit
    countPolynomialTextBox: QLineEdit
    countMemoryRegistersTextBox: QLineEdit
    countExitsTextBox: QLineEdit
    sizeBlockTextBox: QLineEdit
    countBlocksTextBox: QLineEdit

    def __init__(self, parent):
        log.debug("Создание окна добавления кодера")
        super().__init__()
        self.setWindowTitle("Добавление кодера")
        self.sizePackageTextBox = QLineEdit()
        self.listPolynomialTextBox = QLineEdit()
        self.countPolynomialTextBox = QLineEdit()
        self.countMemoryRegistersTextBox = QLineEdit()
        self.countExitsTextBox = QLineEdit()
        self.sizeBlockTextBox = QLineEdit()
        self.countBlocksTextBox = QLineEdit()

        self.setFixedSize(300, 200)
        parent.newCoderWindow = self
        self.windowParent = parent
        self.setWindowIcon(QIcon("Resources/img/AddCoder.png"))

        self.submitButton = QPushButton("Подтвердить")
        self.submitButton.setDisabled(True)
        self.submitButton.setShortcut("Enter")

        self.grid = QGridLayout()
        self.comboBox = QComboBox()
        self.setWindowTitle("Добавить кодер")

        self.comboBox.addItem("Рида-Соломона")
        self.comboBox.addItem("Циклический")
        self.comboBox.addItem("Свёрточный")
        self.comboBox.addItem("Фонтанный")
        self.InitGrid()
        self.setLayout(self.grid)

        self.comboBox.activated[str].connect(self.changeCoder)
        self.submitButton.clicked.connect(self.CreateCoder)

        self.show()

    def InitGrid(self):
        self.grid: QGridLayout = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.comboBox, 0, 0)
        self.grid.addWidget(self.submitButton, 0, 1)
        self.setLayout(self.grid)

    def ReDrawGrid(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        self.grid.addWidget(self.comboBox, 0, 0)
        self.grid.addWidget(self.submitButton, 0, 1)


    def changeCoder(self, text: str):
        self.ReDrawGrid()
        if text == "Рида-Соломона":
            self.grid.addWidget(QLabel("Размер пакета"), 1, 0)
            self.grid.addWidget(self.sizePackageTextBox, 1, 1)
        elif text == "Циклический":
            self.grid.addWidget(QLabel("Размер пакета"), 1, 0)
            self.grid.addWidget(self.sizePackageTextBox, 1, 1)
        elif text == "Свёрточный":
            self.grid.addWidget(QLabel("Количество полиномов"), 1, 0)
            self.grid.addWidget(self.countPolynomialTextBox, 1, 1)
            self.grid.addWidget(QLabel("Список полиномов"), 2, 0)
            self.grid.addWidget(self.listPolynomialTextBox, 2, 1)
            self.grid.addWidget(QLabel("Количество выходов"), 3, 0)
            self.grid.addWidget(self.countExitsTextBox, 3, 1)
            self.grid.addWidget(QLabel("Количество регистров памяти"), 4, 0)
            self.grid.addWidget(self.countMemoryRegistersTextBox, 4, 1)
        elif text == "Фонтанный":
            self.grid.addWidget(QLabel("Размер пакета"), 1, 0)
            self.grid.addWidget(self.sizePackageTextBox, 1, 1)
            self.grid.addWidget(QLabel("Размер блока"), 2, 0)
            self.grid.addWidget(self.sizeBlockTextBox, 2, 1)
            self.grid.addWidget(QLabel("Количество блоков"), 3, 0)
            self.grid.addWidget(self.countBlocksTextBox, 3, 1)
        self.submitButton.setDisabled(False)

    def CreateCoder(self):
        text = self.comboBox.currentText()
        if text == "Рида-Соломона":
            if self.sizePackageTextBox.text().isdigit():
                self.windowParent.SetCoder(hemming.Coder.Coder(
                        int(self.sizePackageTextBox.text())
                        ))
        elif text == "Циклический":
            if self.sizePackageTextBox.text().isdigit():
                self.windowParent.SetCoder(cyclical.Coder.Coder(
                        int(self.sizePackageTextBox.text())
                        ))
        elif text == "Свёрточный":
            if self.countPolynomialTextBox.text().isdigit() and\
                    self.countMemoryRegistersTextBox.text().isdigit() and\
                    self.countExitsTextBox.text().isdigit():
                self.windowParent.SetCoder(convolutional.Coder.Coder(
                        int(self.countPolynomialTextBox.text()),
                        list(self.listPolynomialTextBox.text()),
                        1,
                        int(self.countExitsTextBox.text()),
                        int(self.countMemoryRegistersTextBox.text())
                        ))
        elif text == "Фонтанный":
            if self.sizeBlockTextBox.text().isdigit() and\
                    self.countBlocksTextBox.text().isdigit() and\
                    self.size.sizePackageTextBox.text().isdigit():
                self.windowParent.SetCoder(LubyTransform.Coder(
                        int(self.sizeBlockTextBox.text()),
                        int(self.countBlocksTextBox.text()),
                        int(self.sizePackageTextBox.text())
                        ))

        if self.windowParent.coder is not None:
            del self.windowParent.newCoderWindow
        else:
            QMessageBox.warning(self, "Поля заполнены не верной информацией",
                                "Поля заполнены не верной информацией",
                                QMessageBox.Ok)
