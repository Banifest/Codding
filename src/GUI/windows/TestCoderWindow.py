from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton, QWidget

from src.channel.channel import Channel
from src.coders.casts import IntToBitList
from src.coders.interleaver.Interleaver import Interleaver
from src.logger import log


class TestCoderWindow(QWidget):
    channel: Channel

    noiseProbabilityTextBox: QLineEdit
    countCyclicalTextBox: QLineEdit
    informationTextBox: QLineEdit
    lengthSmashingTextBox: QLineEdit
    duplexCheckBox: QCheckBox
    interleaverCheckBox: QCheckBox

    testingProgressBar: QProgressBar

    lastResult: str = ""

    def __init__(self, parent):
        self.grid = QGridLayout()
        log.debug("Создание окна тестирования кодера")
        super().__init__()
        self.badPackage: int = 0
        self.successfullyPackage: int = 0

        self.setFixedSize(400, 350)
        self.setWindowTitle("Тестирование кодера")
        parent.testCoderWindow = self
        self.windowParent = parent
        self.setWindowIcon(QIcon("Resources/img/TestCoder.jpg"))

        self.submitButton = QPushButton("Начать тестирование")
        self.submitButton.setShortcut("Enter")
        self.lastResultButton = QPushButton("Последний результат")
        self.lastResultButton.setVisible(False)

        self.informationLabel = QLabel("Передаваемая информация")
        self.noiseProbabilityLabel = QLabel("Вероятность искжения бита информации")
        self.countCyclicalLabel = QLabel("Количество попыток передачи при тестировании")
        self.duplexLabel = QLabel("Двунаправленный ли канал?")
        self.interleaverLabel = QLabel("Использование перемежителя")
        self.lengthSmashingLabel = QLabel("Длина раскидования")
        self.progressTestingLabel = QLabel()
        self.progressTestingLabel.setVisible(False)
        self.testingProgressBar = QProgressBar()
        self.testingProgressBar.setVisible(False)

        self.noiseProbabilityTextBox = QLineEdit()
        self.countCyclicalTextBox = QLineEdit()
        self.duplexCheckBox = QCheckBox()
        self.interleaverCheckBox = QCheckBox()
        self.lengthSmashingTextBox = QLineEdit()
        self.informationTextBox = QLineEdit()

        self.lengthSmashingTextBox.setVisible(False)
        self.lengthSmashingLabel.setVisible(False)

        self.InitGrid()

        self.submitButton.clicked.connect(self.StartTest)
        self.interleaverCheckBox.stateChanged.connect(self.CheckIsInterleaver)
        self.lastResultButton.clicked.connect(self.GetLastResult)

        self.show()

    def InitGrid(self):
        log.debug("Иницилизация grid")
        self.grid.addWidget(self.noiseProbabilityLabel, 1, 0)
        self.grid.addWidget(self.noiseProbabilityTextBox, 1, 1)
        self.grid.addWidget(self.countCyclicalLabel, 2, 0)
        self.grid.addWidget(self.countCyclicalTextBox, 2, 1)
        self.grid.addWidget(self.duplexLabel, 3, 0)
        self.grid.addWidget(self.duplexCheckBox, 3, 1)
        self.grid.addWidget(self.interleaverLabel, 4, 0)
        self.grid.addWidget(self.interleaverCheckBox, 4, 1)
        self.grid.addWidget(self.lengthSmashingLabel, 5, 0)
        self.grid.addWidget(self.lengthSmashingTextBox, 5, 1)
        self.grid.addWidget(self.informationLabel, 6, 0)
        self.grid.addWidget(self.informationTextBox, 6, 1)

        self.grid.addWidget(self.submitButton, 7, 0, 1, 2)
        self.grid.addWidget(self.testingProgressBar, 8, 0, 1, 2)
        self.grid.addWidget(self.progressTestingLabel, 9, 0, 1, 2)
        self.grid.addWidget(self.lastResultButton, 10, 0, 1, 2)

        self.grid.setSpacing(10)
        self.setLayout(self.grid)

    def CheckIsInterleaver(self):
        self.lengthSmashingLabel.setVisible(self.interleaverCheckBox.isChecked())
        self.lengthSmashingTextBox.setVisible(self.interleaverCheckBox.isChecked())


    def StartTest(self):
        log.debug("Кнопка тестирования нажата")
        if (self.noiseProbabilityTextBox.text().isdecimal()\
                    or (self.noiseProbabilityTextBox.text().split(".")[0].isdigit()\
                                and self.noiseProbabilityTextBox.text().split(".")[1].isdigit()))\
                and self.countCyclicalTextBox.text().isdigit()\
                and self.informationTextBox.text().isdigit()\
                and (not self.interleaverCheckBox.isChecked() or self.lengthSmashingTextBox.text().isdigit()):
            self.progressTestingLabel.setVisible(True)
            self.testingProgressBar.setVisible(True)

            interleaver: Interleaver
            if self.interleaverCheckBox.isChecked() and self.lengthSmashingTextBox.text().isdigit():
                interleaver = Interleaver(int(self.lengthSmashingTextBox.text()))
            else:
                interleaver = None

            log.debug("Атрибуты проверены на корректность")
            self.channel = Channel(self.windowParent.coder,
                                   int(self.noiseProbabilityTextBox.text()),
                                   int(self.countCyclicalTextBox.text()),
                                   self.duplexCheckBox.isChecked(),
                                   interleaver)

            progress = 0.0
            step = 100.0 / int(self.countCyclicalTextBox.text())
            self.successfullyPackage = 0
            self.badPackage = 0
            log.debug("Начало цикла тестов")
            for x in range(int(self.countCyclicalTextBox.text())):
                self.channel.TransferOneStep(IntToBitList(int(self.informationTextBox.text())))
                self.testingProgressBar.setValue(progress)
                progress += step
                self.progressTestingLabel.setText(str(progress) + "%")
                self.lastResult += self.channel.information
                if self.channel.information == "Пакет при передаче был успешно передан\n":
                    self.successfullyPackage += 1
                else:
                    self.badPackage += 1

            log.debug("Конеци цикла тестов")
            self.testingProgressBar.setValue(100)
            self.progressTestingLabel.setText("100%")
            self.lastResultButton.setVisible(True)
            self.lastResultButton.setShortcut("Ctrl+R")

        else:
            log.debug("Атрибуты указанны некорректно")
            QMessageBox.warning(self, "Неправильно заполнены поля",
                                "Проверте данные введёные в поля",
                                QMessageBox.Ok)


    def GetLastResult(self) -> str:
        QMessageBox.information(self, "Последняя попытка",
                                "Успешно переданно - {0}\n"
                                "Переданно с ошибкой - {1}\n".
                                format(self.successfullyPackage,
                                       self.badPackage),
                                QMessageBox.Ok)
