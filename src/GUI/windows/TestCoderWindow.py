from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget

from src.channel.channel import Channel


class TestCoderWindow(QWidget):
    channel: Channel

    noiseProbabilityTextBox: QLineEdit
    countCyclicalTextBox: QLineEdit
    duplexCheckBox: QCheckBox
    interleaverTextBox: QLineEdit


    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(300, 200)
        parent.testCoderWindow = self
        self.windowParent = parent
        self.setWindowIcon(QIcon("Resources/img/TestCoder.jpg"))

        self.submitButton = QPushButton("Начать тестирование")

        self.noiseProbabilityLabel = QLabel("Вероятность искжения бита информации")
        self.countCyclicalLabel = QLabel("Количество попыток передачи при тестировании")
        self.duplexLabel = QLabel("Двунаправленный ли канал?")
        self.interleaverLabel = QLabel("Использование перемежителя")

        self.noiseProbabilityTextBox = QLineEdit()
        self.countCyclicalTextBox = QLineEdit()
        self.duplexCheckBox = QCheckBox()
        self.interleaverTextBox = QLineEdit()

        self.InitGrid()

        self.submitButton.clicked.connect(self.StartTest)
        self.show()

    def InitGrid(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.noiseProbabilityLabel, 1, 0)
        self.grid.addWidget(self.noiseProbabilityTextBox, 1, 1)
        self.grid.addWidget(self.countCyclicalLabel, 2, 0)
        self.grid.addWidget(self.countCyclicalTextBox, 2, 1)
        self.grid.addWidget(self.duplexLabel, 3, 0)
        self.grid.addWidget(self.duplexCheckBox, 3, 1)
        self.grid.addWidget(self.interleaverLabel, 4, 0)
        self.grid.addWidget(self.interleaverTextBox, 4, 1)

        self.grid.addWidget(self.submitButton, 5, 0)

        self.grid.setSpacing(10)
        self.setLayout(self.grid)

    def StartTest(self):
        print("lol kek cheburek")
