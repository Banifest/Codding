import os
import threading
from random import randint

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton, QWidget

from src.GUI.graphics import DrawGraphic
from src.channel.cascade import Cascade
from src.channel.channel import Channel
from src.coders import cyclical, hemming
from src.coders.casts import IntToBitList
from src.coders.interleaver.Interleaver import Interleaver
from src.logger import log


class TestCascadeCoderWindow(QWidget):
    channel: Channel
    cascade: Cascade

    noiseProbabilityTextBox: QLineEdit
    countCyclicalTextBox: QLineEdit
    informationTextBox: QLineEdit
    lengthSmashingTextBox: QLineEdit
    duplexCheckBox: QCheckBox
    interleaverCheckBox: QCheckBox

    interleaverLabelSecond: QLabel
    lengthSmashingLabelSecond: QLabel

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

        self.setFixedSize(600, 350)
        self.setWindowTitle("Тестирование кодера")
        parent.testCoderWindow = self
        self.windowParent = parent
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

        self.interleaverLabelSecond = QLabel("Использование перемежителя второго кодера")
        self.lengthSmashingLabelSecond = QLabel("Длина раскидования")

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

        self.interleaverCheckBoxSecond = QCheckBox()
        self.lengthSmashingTextBoxSecond = QLineEdit()

        self.lengthSmashingTextBoxSecond.setVisible(False)
        self.lengthSmashingLabelSecond.setVisible(False)

        self.InitGrid()

        self.submitButton.clicked.connect(self.StartTest)
        self.autoTestButton.clicked.connect(self.AutoTest)
        self.interleaverCheckBox.stateChanged.connect(self.CheckIsInterleaver)
        self.interleaverCheckBoxSecond.stateChanged.connect(self.CheckIsInterleaverSecond)
        self.lastResultButton.clicked.connect(self.GetLastResult)

        self.show()

    def InitGrid(self):
        log.debug("Иницилизация grid")
        self.grid.addWidget(self.noiseProbabilityLabel, 1, 0)
        self.grid.addWidget(self.noiseProbabilityTextBox, 1, 2, 1, 2)
        self.grid.addWidget(self.countCyclicalLabel, 2, 0)
        self.grid.addWidget(self.countCyclicalTextBox, 2, 2, 1, 2)
        self.grid.addWidget(self.duplexLabel, 3, 0)
        self.grid.addWidget(self.duplexCheckBox, 3, 2, 1, 2)
        self.grid.addWidget(self.interleaverLabel, 4, 0)
        self.grid.addWidget(self.interleaverCheckBox, 4, 1)
        self.grid.addWidget(self.interleaverLabelSecond, 4, 2)
        self.grid.addWidget(self.interleaverCheckBoxSecond, 4, 3)
        self.grid.addWidget(self.lengthSmashingLabel, 5, 0)
        self.grid.addWidget(self.lengthSmashingTextBox, 5, 1, 1, 1)
        self.grid.addWidget(self.lengthSmashingTextBoxSecond, 5, 3, 1, 1)
        self.grid.addWidget(self.informationLabel, 6, 0)
        self.grid.addWidget(self.informationTextBox, 6, 2, 1, 2)

        self.grid.addWidget(self.submitButton, 7, 0, 1, 4)
        self.grid.addWidget(self.autoTestButton, 8, 0, 1, 4)
        self.grid.addWidget(self.testingProgressBar, 9, 0, 1, 4)
        self.grid.addWidget(self.autoTestingProgressBar, 10, 0, 1, 4)
        self.grid.addWidget(self.lastResultButton, 11, 0, 1, 4)

        self.grid.setSpacing(10)
        self.setLayout(self.grid)

    def CheckIsInterleaverSecond(self):
        self.lengthSmashingLabel.setVisible(self.interleaverCheckBoxSecond.isChecked())
        self.lengthSmashingTextBoxSecond.setVisible(self.interleaverCheckBoxSecond.isChecked())

        #  def StartTestThread(self):
        #     threading.Thread(target=StartTest, name="Start Test", args=(self,)).start()

    def AutoTestThread(self):
        threading.Thread(target=self.AutoTest, name="Auto Test").start()

    def CheckIsInterleaver(self):
        self.lengthSmashingLabel.setVisible(self.interleaverCheckBox.isChecked())
        self.lengthSmashingTextBox.setVisible(self.interleaverCheckBox.isChecked())

    def TestOnCorrectData(self) -> bool:
        return (self.noiseProbabilityTextBox.text().isdecimal()\
                or (len(self.noiseProbabilityTextBox.text().split(".")) == 2\
                    and self.noiseProbabilityTextBox.text().split(".")[0].isdigit()\
                    and self.noiseProbabilityTextBox.text().split(".")[1].isdigit()))\
               and self.countCyclicalTextBox.text().isdigit()\
               and self.informationTextBox.text().isdigit()\
               and (not self.interleaverCheckBox.isChecked() or self.lengthSmashingTextBox.text().isdigit())

    def CycliTest(self):
        pass

    def StartTest(self, flag=None, testInformation=None):
        log.debug("Кнопка тестирования нажата")
        if self.TestOnCorrectData():
            self.autoTestButton.setEnabled(False)
            self.lastResultButton.setEnabled(False)
            self.submitButton.setEnabled(False)

            interleaver: Interleaver
            if self.interleaverCheckBox.isChecked() and self.lengthSmashingTextBox.text().isdigit():
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
            information: list
            if type(testInformation.__class__) != type(list):
                information = testInformation
            elif type(self.channel.coder.__class__) == type(hemming.Coder.Coder)\
                    or type(self.channel.coder.__class__) == type(cyclical.Coder.Coder):
                information = IntToBitList(int(self.informationTextBox.text()),
                                           self.channel.coder.lengthInformation)
            else:
                information = IntToBitList(int(self.informationTextBox.text()))
            log.debug("Начало цикла тестов")
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
            QMessageBox.warning(self, "Неправильно заполнены поля"
                                      "Проверте данные введёные в поля",
                                QMessageBox.Ok)

    def AutoTest(self):
        log.debug("Кнопка авто-тестирования нажата")
        if self.TestOnCorrectData():
            # self.testingProgressBar.setVisible(False)
            self.autoTestingProgressBar.setVisible(True)
            self.noiseProbabilityTextBox.setEnabled(False)

            status: float = 0
            start: int = 0
            finish: int = 20
            step: float = 100 / (finish - start)

            drawData: list = []
            for x in range(start, finish):
                self.noiseProbabilityTextBox.setText(str(x))
                information: list
                status += step
                if type(self.windowParent.coder.__class__) == type(hemming.Coder.Coder)\
                        or type(self.windowParent.coder.__class__) == type(cyclical.Coder.Coder):
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
            QMessageBox.warning(self, "Неправильно заполнены поля",
                                "Проверте данные введёные в поля",
                                QMessageBox.Ok)

    def GetLastResult(self) -> str:
        choise = QMessageBox.information(self, "Последняя попытка\n",
                                         "Успешно переданно (пакет не исказился) - {0}\n"
                                         "Успешно исправленно паккетов - {1}\n"
                                         "Переданно с ошибкой - {2}\n".
                                         format(self.successfullyPackage,
                                                self.repairPackage,
                                                self.badPackage + self.invisiblePackage),
                                         QMessageBox.Ok | QMessageBox.Help,
                                         QMessageBox.Ok)

        if choise == QMessageBox.Help:
            os.system("lastInformation.txt")
            pass


    def StartTest(self, flag=None, testInformation=None):
        log.debug("(КАСКАД)Кнопка тестирования нажата")
        if self.TestOnCorrectData():
            self.autoTestButton.setEnabled(False)
            self.lastResultButton.setEnabled(False)
            self.submitButton.setEnabled(False)

            interleaver: Interleaver
            if self.interleaverCheckBox.isChecked() and self.lengthSmashingTextBox.text().isdigit():
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
            information: list
            if type(testInformation.__class__) != type(list):
                information = testInformation
            elif type(self.channel.coder.__class__) == type(hemming.Coder.Coder)\
                    or type(self.channel.coder.__class__) == type(cyclical.Coder.Coder):
                information = IntToBitList(int(self.informationTextBox.text()),
                                           self.channel.coder.lengthInformation)
            else:
                information = IntToBitList(int(self.informationTextBox.text()))
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
            QMessageBox.warning(self, "Неправильно заполнены поля"
                                      "Проверте данные введёные в поля",
                                QMessageBox.Ok)
