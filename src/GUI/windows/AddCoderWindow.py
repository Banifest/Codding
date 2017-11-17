from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QRadioButton, QWidget
from PyQt5.uic import loadUi

from src.logger import log


class AddCoderWindow(QWidget):
    sizePackageTextBox: QLineEdit
    listPolynomialTextBox: QLineEdit
    countPolynomialTextBox: QLineEdit
    countMemoryRegistersTextBox: QLineEdit
    countExitsTextBox: QLineEdit
    sizeBlockTextBox: QLineEdit
    countBlocksTextBox: QLineEdit

    firstCoderRadioButton: QRadioButton
    secondCoderRadioButton: QRadioButton

    def __init__(self, controller):
        super().__init__()

        log.debug("Создание окна добавления кодера")
        self.controller = controller
        loadUi(r'src\GUI\UI\adding_coder.ui', self)

        self.sizePackageTextBox: QLineEdit = QLineEdit("120")
        self.listPolynomialTextBox: QLineEdit = QLineEdit("3, 5, 7")
        self.countPolynomialTextBox: QLineEdit = QLineEdit("3")
        self.countMemoryRegistersTextBox: QLineEdit = QLineEdit("3")
        self.countExitsTextBox: QLineEdit = QLineEdit("2")
        self.sizeBlockTextBox: QLineEdit = QLineEdit("10")
        self.countBlocksTextBox: QLineEdit = QLineEdit("30")
        self.powerReedMullerTextBox = QLineEdit("2")
        self.maxLengthRecoverPackageTextBox = QLineEdit("3")

        self.sizePackageTextBox.setValidator(QIntValidator())
        # self.listPolynomialTextBox.setValidator(QIntValidator())
        self.countPolynomialTextBox.setValidator(QIntValidator())
        self.countMemoryRegistersTextBox.setValidator(QIntValidator())
        self.countExitsTextBox.setValidator(QIntValidator())
        self.sizeBlockTextBox.setValidator(QIntValidator())
        self.countBlocksTextBox.setValidator(QIntValidator())
        self.powerReedMullerTextBox.setValidator(QIntValidator())
        self.maxLengthRecoverPackageTextBox.setValidator(QIntValidator())

        self.choose_comboBox.activated[str].connect(self.change_coder)
        self.submit_button.clicked.connect(self.controller.set_coder)

        self.show()

    def redraw_grid(self) -> None:
        for i in reversed(range(self.grid_coder_options.count())):
            self.grid_coder_options.itemAt(i).widget().setParent(None)

    def change_coder(self, text: str):
        self.redraw_grid()
        if text == "Хемминга":
            self.grid_coder_options.addWidget(QLabel("Размер пакета"), 2, 0)
            self.grid_coder_options.addWidget(self.sizePackageTextBox, 2, 1)
        elif text == "Циклический":
            self.grid_coder_options.addWidget(QLabel("Размер пакета"), 2, 0)
            self.grid_coder_options.addWidget(self.sizePackageTextBox, 2, 1)
            self.grid_coder_options.addWidget(QLabel("Порождающий полином"), 3, 0)
            self.listPolynomialTextBox: QLineEdit = QLineEdit("13")
            self.grid_coder_options.addWidget(self.listPolynomialTextBox, 3, 1)
        elif text == "Сверточный":
            self.grid_coder_options.addWidget(QLabel("Список полиномов"), 3, 0)
            self.listPolynomialTextBox: QLineEdit = QLineEdit("3, 5, 7")
            self.grid_coder_options.addWidget(self.listPolynomialTextBox, 3, 1)
            self.grid_coder_options.addWidget(QLabel("Количество регистров памяти"), 4, 0)
            self.grid_coder_options.addWidget(self.countMemoryRegistersTextBox, 4, 1)
        elif text == "Фонтанный":
            self.grid_coder_options.addWidget(QLabel("Размер пакета"), 2, 0)
            self.grid_coder_options.addWidget(self.sizePackageTextBox, 2, 1)
            self.grid_coder_options.addWidget(QLabel("Размер блока"), 3, 0)
            self.grid_coder_options.addWidget(self.sizeBlockTextBox, 3, 1)
            self.grid_coder_options.addWidget(QLabel("Количество блоков"), 4, 0)
            self.grid_coder_options.addWidget(self.countBlocksTextBox, 4, 1)
        elif text == 'Рида-Маллера':
            self.grid_coder_options.addWidget(QLabel("Размер пакета"), 2, 0)
            self.grid_coder_options.addWidget(self.sizePackageTextBox, 2, 1)

            # я не знаю как корректно описать это поле
            self.grid_coder_options.addWidget(QLabel("Степень кодера"), 3, 0)
            self.grid_coder_options.addWidget(self.powerReedMullerTextBox, 3, 1)
        elif text == 'Сверточный для пакетов':
            self.grid_coder_options.addWidget(QLabel("Макс длина исправляемого пакета"), 2, 0)
            self.grid_coder_options.addWidget(self.maxLengthRecoverPackageTextBox, 2, 1)
            self.grid_coder_options.addWidget(QLabel("Список полиномов"), 3, 0)
            self.grid_coder_options.addWidget(self.listPolynomialTextBox, 3, 1)
            self.grid_coder_options.addWidget(QLabel("Количество регистров памяти"), 4, 0)
            self.grid_coder_options.addWidget(self.countMemoryRegistersTextBox, 4, 1)

        self.submit_button.setDisabled(text == 'Выбор кодера')
