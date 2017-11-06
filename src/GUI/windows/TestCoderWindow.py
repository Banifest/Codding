import os
import threading
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QLineEdit, QMessageBox, QProgressBar, QPushButton, QWidget

from coders.interleaver import Interleaver
from src.GUI.graphics import draw_graphic, draw_plot_pie
from src.channel.channel import Channel
from src.coders import convolutional, cyclical, linear
from src.coders.casts import IntToBitList
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

    def __init__(self, controller):
        self.grid = QGridLayout()
        log.debug("Создание окна тестирования кодера")
        super().__init__()
        self.controller = controller
        uic.loadUi(r'src\GUI\UI\test_simple_coder.ui', self)

        self.noise_text_box.setValidator(QDoubleValidator())
        self.count_test_text_box.setValidator(QIntValidator())

        self.begin_test_button.pushButton.connect(self.controller)
        self.show()

    def AutoTestThread(self):
        threading.Thread(target=self.AutoTest, name="Auto Test").start()

    def CheckIsInterleaver(self):
        self.lengthSmashingLabel.setVisible(self.interleaverCheckBox.isChecked())
        self.lengthSmashingTextBox.setVisible(self.interleaverCheckBox.isChecked())

    def AutoTest(self):
        log.debug("Кнопка авто-тестирования нажата")
        if self.TestOnCorrectData():
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
            draw_graphic(drawData, self.windowParent.coder_name, self.windowParent.coder)
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
            draw_plot_pie([self.successfullyPackage, self.repairPackage, self.badPackage + self.invisiblePackage])

    def StartTest(self, flag=None, testInformation=None):
        log.debug("Кнопка тестирования нажата")
        if self.CheckOnCorrectTransferData():
            return
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
            elif isinstance(self.channel.coder, linear.hemming.Coder)\
                    or isinstance(self.channel.coder, cyclical.Coder.Coder):
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
