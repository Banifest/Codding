import os
from random import randint

from PyQt5 import uic
from PyQt5.QtWidgets import QCheckBox, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton, QWidget

from coders.interleaver import Interleaver
from src.GUI.graphics import draw_graphic, draw_plot_pie
from src.channel.cascade import Cascade
from src.channel.channel import Channel
from src.coders import convolutional, cyclical, linear
from src.coders.casts import IntToBitList
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

    def __init__(self, controller):
        log.debug("Создание окна тестирования кодера")
        super().__init__()

        uic.loadUi(r'src\GUI\UI\test_cascade_coder.ui', self)
        self.controller = controller
        self.controller._testCascadeCoderWindow = self

        self.show()

    def TestOnCorrectData(self) -> bool:
        return (self.noiseProbabilityTextBox.text().isdecimal()\
                or (len(self.noiseProbabilityTextBox.text().split(".")) == 2\
                    and self.noiseProbabilityTextBox.text().split(".")[0].isdigit()\
                    and self.noiseProbabilityTextBox.text().split(".")[1].isdigit()))\
               and self.countCyclicalTextBox.text().isdigit()\
               and self.informationTextBox.text().isdigit()\
               and (not self.interleaverCheckBox.isChecked() or self.lengthSmashingTextBox.text().isdigit())

    def StartTest(self, flag=None, testInformation=None):
        log.debug("Кнопка тестирования нажата")
        if self.CheckOnCorrectTransferData():
            return
        if self.TestOnCorrectData():
            self.autoTestButton.setEnabled(False)
            self.lastResultButton.setEnabled(False)
            self.submitButton.setEnabled(False)

            interleaver: Interleaver
            if self.interleaverCheckBox.isChecked() and self.lengthSmashingTextBox.text().isdigit():
                interleaver = Interleaver(int(self.lengthSmashingTextBox.text()))
            else:
                interleaver = None

            if self.interleaverCheckBoxSecond.isChecked() and self.lengthSmashingTextBoxSecond.text().isdigit():
                interleaverSecond = Interleaver(int(self.lengthSmashingTextBox.text()))
            else:
                interleaverSecond = None

            log.debug("Атрибуты проверены на корректность")
            self.cascade = Cascade(self.windowParent.firstCoder,
                                   self.windowParent.secondCoder,
                                   float(self.noiseProbabilityTextBox.text()),
                                   int(self.countCyclicalTextBox.text()),
                                   self.duplexCheckBox.isChecked(),
                                   interleaver,
                                   interleaverSecond)


            progress = 0.0
            step = 100.0 / int(self.countCyclicalTextBox.text())
            self.successfullyPackage = 0
            self.badPackage = 0
            self.repairPackage = 0
            self.invisiblePackage = 0
            information: list

            if isinstance(testInformation, list):
                information = testInformation
            elif isinstance(self.cascade.firstCoder, linear.hemming.Coder)\
                    or isinstance(self.cascade.firstCoder, cyclical.Coder.Coder):
                information = IntToBitList(int(self.informationTextBox.text()),
                                           self.cascade.firstCoder.lengthInformation)
            else:
                information = IntToBitList(int(self.informationTextBox.text()))

            log.debug("Начало цикла тестов")
            for x in range(int(self.countCyclicalTextBox.text())):
                status: int = self.cascade.GetTransferOneStep(information)
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
                #   self.lastResult += self.cascade.information

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
                information = randint(0, 1 << self.windowParent.firstCoder.lengthInformation)
                self.StartTest()
                #                information = IntToBitList(int(self.informationTextBox.text()))
                drawData.append(self.StartTest(testInformation=information))
                self.autoTestingProgressBar.setValue(int(status))
            self.noiseProbabilityTextBox.setEnabled(True)
            draw_graphic(drawData, self.windowParent.coderName, self.windowParent.coder)
        else:
            log.debug("Атрибуты указанны некорректно")
            msg = QMessageBox()
            msg.setWindowTitle("Неправильно заполнены поля")
            msg.setText("Проверьте правильность заполнения полей")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def GetLastResult(self) -> str:
        choise = QMessageBox.information(self, "Последняя попытка\n",
                                         "Успешно переданно (пакет не исказился) - {0}\n"
                                         "Успешно исправленно паккетов - {1}\n"
                                         "Переданно с ошибкой - {2}\n".
                                         format(self.successfullyPackage,
                                                self.repairPackage,
                                                self.badPackage + self.invisiblePackage),
                                         QMessageBox.Ok | QMessageBox.Help | QMessageBox.Open,
                                         QMessageBox.Ok)

        if choise == QMessageBox.Open:
            os.system("lastInformation.txt")
            draw_plot_pie([self.successfullyPackage, self.repairPackage, self.badPackage + self.invisiblePackage])
        elif choise == QMessageBox.Help:
            a = 0
            msg = QMessageBox()
            msg.setWindowTitle("Информация о каскадном кодере")
            msg.setText("Кодер типа - каскадный\n"
                        "Избыточность информации- {0}%\n"
                        "Скорость кодера - {1}\n".format(
                    (self.windowParent.firstCoder.GetRedundancy() + 100) * (
                        self.windowParent.secondCoder.GetRedundancy() + 100) / 100 - 1,
                    (self.windowParent.firstCoder.GetSpeed() * self.windowParent.secondCoder.GetSpeed())
                    ))
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


    def StartTest(self, flag=None, testInformation=None):
        log.debug("(КАСКАД)Кнопка тестирования нажата")
        if self.TestOnCorrectData():
            if self.CheckOnCorrectTransferData():
                return
            self.autoTestButton.setEnabled(False)
            self.lastResultButton.setEnabled(False)
            self.submitButton.setEnabled(False)

            interleaver: Interleaver
            if self.interleaverCheckBox.isChecked() and self.lengthSmashingTextBox.text().isdigit() and\
                            self.lengthSmashingTextBox.text()[0] != "0":
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
        if self.windowParent.firstCoder.lengthInformation < len(IntToBitList(int(self.informationTextBox.text())))\
                and not isinstance(self.windowParent.firstCoder, convolutional.Coder.Coder) and\
                        self.windowParent.secondCoder.lengthInformation < len(
                        IntToBitList(int(self.informationTextBox.text())))\
                and not isinstance(self.windowParent.secondCoder, convolutional.Coder.Coder):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Неправильно заполнены поле передаваемого пакета")
            msg.setText("Проверьте правильность заполнения полей")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return True
        else:
            return False
