import os
import threading
from random import randint

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton, QWidget

from src.GUI.graphics import DrawGraphic
from src.GUI.windows import MainWindow
from src.channel.channel import Channel
from src.coders import convolutional, cyclical, hemming
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
    autoTestingProgressBar: QProgressBar

    submitButton: QPushButton
    lastResultButton: QPushButton
    autoTestButton: QPushButton

    lastResult: str = ""

    def __init__(self, parent):
        self.grid = QGridLayout()
        log.debug("Создание окна тестирования кодера")
        super().__init__()
        self.badPackage: int = 0
        self.successfullyPackage: int = 0
        self.repairPackage: int = 0
        self.invisiblePackage: int = 0

        self.setFixedSize(400, 350)
        self.setWindowTitle("Тестирование кодера")
        parent.testCoderWindow = self
        self.windowParent: MainWindow.MainWindow = parent
        self.setWindowIcon(QIcon("Resources/img/TestCoder.jpg"))

        self.submitButton = QPushButton("Начать тестирование")
        self.submitButton.setShortcut("Enter")
        self.lastResultButton = QPushButton("Последний результат")
        self.lastResultButton.setVisible(False)
        self.autoTestButton = QPushButton("Авто тестирование")

        self.informationLabel = QLabel("Передаваемая информация")
        self.noiseProbabilityLabel = QLabel("Вероятность искжения бита информации")
        self.countCyclicalLabel = QLabel("Количество попыток передачи при тестировании")
        self.duplexLabel = QLabel("Двунаправленный ли канал?")
        self.interleaverLabel = QLabel("Использование перемежителя")
        self.lengthSmashingLabel = QLabel("Длина раскидования")

        self.testingProgressBar = QProgressBar()
        self.autoTestingProgressBar = QProgressBar()
        self.autoTestingProgressBar.setVisible(False)

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
        self.autoTestButton.clicked.connect(self.AutoTest)
        self.interleaverCheckBox.stateChanged.connect(self.CheckIsInterleaver)
        self.lastResultButton.clicked.connect(self.GetLastResult)

        self.show()

    def InitGrid(self):
        log.debug("Иницилизация grid")
        self.grid.addWidget(self.noiseProbabilityLabel, 1, 0)
        self.grid.addWidget(self.noiseProbabilityTextBox, 1, 1)
        self.grid.addWidget(self.countCyclicalLabel, 2, 0)
        self.grid.addWidget(self.countCyclicalTextBox, 2, 1)
        self.grid.addWidget(self.interleaverLabel, 4, 0)
        self.grid.addWidget(self.interleaverCheckBox, 4, 1)
        self.grid.addWidget(self.lengthSmashingLabel, 5, 0)
        self.grid.addWidget(self.lengthSmashingTextBox, 5, 1)
        self.grid.addWidget(self.informationLabel, 6, 0)
        self.grid.addWidget(self.informationTextBox, 6, 1)

        self.grid.addWidget(self.submitButton, 7, 0, 1, 2)
        self.grid.addWidget(self.autoTestButton, 8, 0, 1, 2)
        self.grid.addWidget(self.testingProgressBar, 9, 0, 1, 2)
        self.grid.addWidget(self.autoTestingProgressBar, 10, 0, 1, 2)
        self.grid.addWidget(self.lastResultButton, 11, 0, 1, 2)

        self.grid.setSpacing(10)
        self.setLayout(self.grid)

        #  def StartTestThread(self):
        #      threading.Thread(target=StartTest, name="Start Test", args=(self,)).start()

    def AutoTestThread(self):
        threading.Thread(target=self.AutoTest, name="Auto Test").start()

    def CheckIsInterleaver(self):
        self.lengthSmashingLabel.setVisible(self.interleaverCheckBox.isChecked())
        self.lengthSmashingTextBox.setVisible(self.interleaverCheckBox.isChecked())

    def TestOnCorrectData(
            self) -> bool:  # Убил бы, если увидел у другого, но тут я сам....(ПЕРЕПИСАТЬ!!!)з.ы. даже в туду стыдно ставить
        return (self.noiseProbabilityTextBox.text().isdecimal()\
                or (len(self.noiseProbabilityTextBox.text().split(".")) == 2\
                    and self.noiseProbabilityTextBox.text().split(".")[0].isdigit()\
                    and self.noiseProbabilityTextBox.text().split(".")[1].isdigit()))\
               and self.countCyclicalTextBox.text().isdigit() and self.countCyclicalTextBox.text()[0] != "0"\
               and self.informationTextBox.text().isdigit() and self.informationTextBox.text()[0] != "0"\
               and (not self.interleaverCheckBox.isChecked() or
                    (self.lengthSmashingTextBox.text().isdigit() and self.lengthSmashingTextBox.text()[0] != "0"))


    def AutoTest(self):
        log.debug("Кнопка авто-тестирования нажата")
        if self.TestOnCorrectData():
            # self.testingProgressBar.setVisible(False)
            self.autoTestingProgressBar.setVisible(True)
            self.noiseProbabilityTextBox.setEnabled(False)

            if self.CheckOnCorrectTransferData():
                return

            status: float = 0
            start: int = 0
            finish: int = 20
            step: float = 100 / (finish - start)

            drawData: list = []
            for x in range(start, finish):
                self.noiseProbabilityTextBox.setText(str(x))
                information: list
                status += step
                if isinstance(self.windowParent.coder, cyclical.Coder.Coder):
                    information = randint(0, 1 << self.windowParent.coder.lengthInformation)
                    self.StartTest()
                else:
                    information = IntToBitList(int(self.informationTextBox.text()))
                drawData.append(self.StartTest(testInformation=information))
                self.autoTestingProgressBar.setValue(int(status))
            self.noiseProbabilityTextBox.setEnabled(True)
            DrawGraphic(drawData)
        else:
            log.debug("Атрибуты указанны некорректно")
            msg = QMessageBox()
            msg.setWindowTitle("Неправильно заполнены поля")
            msg.setText("Проверьте правильность заполнения полей")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def GetLastResult(self) -> None:
        choise = QMessageBox.information(self, "Последняя попытка\n",
                                         "Успешно переданно (пакет не исказился) - {0}\n"
                                         "Успешно исправленно паккетов - {1}\n"
                                         "Переданно с ошибкой - {2}\n".
                                         format(self.successfullyPackage,
                                                self.repairPackage,
                                                self.badPackage + self.invisiblePackage),
                                         QMessageBox.Ok | QMessageBox.Open,
                                         QMessageBox.Ok)

        if choise == QMessageBox.Open:
            os.system("lastInformation.txt")


    def StartTest(self, flag=None, testInformation=None):
        log.debug("Кнопка тестирования нажата")
        if self.TestOnCorrectData():
            self.autoTestButton.setEnabled(False)
            self.lastResultButton.setEnabled(False)
            self.submitButton.setEnabled(False)

            interleaver: Interleaver
            if self.interleaverCheckBox.isChecked() and self.lengthSmashingTextBox.text().isdigit()\
                    and self.lengthSmashingTextBox.text()[0] != "0":
                interleaver = Interleaver(int(self.lengthSmashingTextBox.text()))
            else:
                interleaver = None

            log.debug("Атрибуты проверены на корректность")
            self.channel = Channel(self.windowParent.coder,
                                   float(self.noiseProbabilityTextBox.text()),
                                   int(self.countCyclicalTextBox.text()),
                                   self.duplexCheckBox.isChecked(),
                                   interleaver)

            progress = 0.0
            step = 100.0 / int(self.countCyclicalTextBox.text())
            self.successfullyPackage = 0
            self.badPackage = 0
            self.repairPackage = 0
            self.invisiblePackage = 0
            information: list = []

            if isinstance(testInformation, list):
                information = testInformation
            elif isinstance(self.channel.coder, hemming.Coder.Coder)\
                    or isinstance(self.channel.coder, cyclical.Coder.Coder):
                information = IntToBitList(int(self.informationTextBox.text()),
                                           self.channel.coder.lengthInformation)
            else:
                information = IntToBitList(int(self.informationTextBox.text()))

            if self.CheckOnCorrectTransferData():
                return

            log.debug("Начало цикла тестов")
            writer = open("lastInformation.txt", "w")
            for x in range(int(self.countCyclicalTextBox.text())):
                status: int = self.channel.TransferOneStep(information)
                if status == 0:
                    self.successfullyPackage += 1
                elif status == 1:
                    self.repairPackage += 1
                elif status == 2:
                    self.badPackage += 1
                else:
                    self.invisiblePackage += 1
                writer.write(self.channel.information)
                self.testingProgressBar.setValue(progress)
                progress += step
                self.lastResult += self.channel.information

            log.debug("Конец цикла тестов")
            self.testingProgressBar.setValue(100)
            self.lastResultButton.setVisible(True)
            self.lastResultButton.setShortcut("Ctrl+R")

            self.autoTestButton.setEnabled(True)
            self.lastResultButton.setEnabled(True)
            self.submitButton.setEnabled(True)
            return [self.successfullyPackage, self.repairPackage, self.badPackage, self.invisiblePackage]

        else:
            log.debug("Атрибуты указанны некорректно")
            msg = QMessageBox()
            msg.setWindowTitle("Неправильно заполнены поля")
            msg.setText("Проверьте правильность заполнения полей")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


    def CheckOnCorrectTransferData(self) -> bool:
        if self.windowParent.coder.lengthInformation < len(IntToBitList(int(self.informationTextBox.text())))\
                and not isinstance(self.windowParent.coder, convolutional.Coder.Coder):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Неправильно заполнены поле передаваемого пакета")
            msg.setText("Проверьте правильность заполнения полей")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return True
        else:
            return False
