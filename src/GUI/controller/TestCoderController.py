import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget

from GUI.graphics import draw_graphic, draw_plot_pie
from GUI.windows.TestCoderWindow import TestCoderWindow
# noinspection PyAttributeOutsideInit
from coders.abstractCoder import AbstractCoder
from coders.casts import IntToBitList
from coders.interleaver import Interleaver
from src.channel.channel import Channel
from src.logger import log


class TestCoderController:
    _testCoderWindow: TestCoderWindow
    _mainController: None
    _lastResult: str = ""

    def __init__(self, _main_controller):
        self._mainController = _main_controller

    def set_window(self, testCoderWindow):
        self._testCoderWindow = testCoderWindow

    def enable_disable_widget(self, param: bool):
        self._testCoderWindow.get_last_result_button.setEnabled(param)
        self._testCoderWindow.noise_text_box.setEnabled(param)
        self._testCoderWindow.count_test_text_box.setEnabled(param)
        self._testCoderWindow.is_interleaver_first.setEnabled(param)
        self._testCoderWindow.information_text_box.setEnabled(param)
        self._testCoderWindow.begin_test_button.setEnabled(param)
        self._testCoderWindow.begin_auto_test_button.setEnabled(param)
        if self._testCoderWindow.first_length_text_box.isEnabled():
            self._testCoderWindow.first_length_text_box.setEnabled(param)

    # необходимо для наследования
    # noinspection PyAttributeOutsideInit
    def set_thread_class(self):
        self._threadClass = TestCoder(self._testCoderWindow, self._mainController.currentCoder, self._lastResult)

    def starting_test(self, param: bool):
        try:
            self.set_thread_class()
            self.enable_disable_widget(False)
            self._threadClass.set_auto(param)

            self._threadClass.autoStepFinished.connect(lambda val: self._testCoderWindow.auto_test.setValue(val))
            self._threadClass.stepFinished.connect(lambda val: self._testCoderWindow.single_test.setValue(val))
            self._threadClass.ended.connect(lambda: self.enable_disable_widget(True))
            self._threadClass.start()
        except:
            QMessageBox.warning(self._testCoderWindow,
                                "Проверте параметры на корректность информации",
                                "Ошибочно заполнены поля параметров",
                                QMessageBox.Ok,
                                QMessageBox.Ok)

    def get_last_result(self):
        msg = QMessageBox.information(self._testCoderWindow,
                                      "Последняя попытка\n",
                                      "Успешно переданно (пакет не исказился) - {0}\n"
                                      "Успешно исправленно паккетов - {1}\n"
                                      "Переданно с ошибкой - {2}\n".
                                      format(self._threadClass.successfullyPackage,
                                             self._threadClass.repairPackage,
                                             self._threadClass.badPackage + self._threadClass.invisiblePackage),
                                      QMessageBox.Ok | QMessageBox.Open,
                                      QMessageBox.Ok)
        if msg == QMessageBox.Open:
            os.system("lastInformation.txt")
            draw_plot_pie([self._threadClass.successfullyPackage, self._threadClass.repairPackage,
                           self._threadClass.badPackage + self._threadClass.invisiblePackage])


class TestCoder(QThread):
    stepFinished = pyqtSignal('int')
    autoStepFinished = pyqtSignal('int')
    ended = pyqtSignal()

    noiseChance: float = 0
    countTest: int = 1
    information: int = 1
    currentCoder: AbstractCoder
    is_auto: bool = False
    is_interleaver: bool = False
    first_length_interleaver: int = 1

    def __init__(self, test_window: QWidget, currentCoder: AbstractCoder, lastResult: str):
        super(TestCoder, self).__init__(None)
        self.successfullyPackage = 0
        self.badPackage = 0
        self.repairPackage = 0
        self.invisiblePackage = 0
        self.lastResult = lastResult
        self.currentCoder = currentCoder
        self.noiseChance = float(test_window.noise_text_box.text())
        self.countTest = int(test_window.count_test_text_box.text())
        self.information = int(test_window.information_text_box.text())
        self.speed = self.currentCoder.get_speed()
        self.coderName = self.currentCoder.name

        self.channel = Channel(
                self.currentCoder,
                self.noiseChance,
                self.countTest,
                False,
                Interleaver.Interleaver(int(test_window.first_length_text_box.text()))
                if test_window.is_interleaver_first.isChecked() else None)

    def __del__(self):
        self.wait()

    def set_auto(self, flag: bool):
        self.is_auto = flag

    def one_test(self):
        progress = 0.0
        step = 100.0 / self.countTest
        information: list = IntToBitList(self.information)

        log.debug("Начало цикла тестов")
        writer = open("lastInformation.txt", "w")
        for x in range(self.countTest):
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
            progress += step
            self.lastResult += self.channel.information
            self.stepFinished.emit(int(progress))

    def auto_test(self):
        log.debug("Кнопка авто-тестирования нажата")
        status: float = 0
        start: int = 0
        finish: int = 20
        step: float = 100 / (finish - start)

        draw_data: list = []
        for x in range(start, finish):
            self.successfullyPackage = 0
            self.badPackage = 0
            self.repairPackage = 0
            self.invisiblePackage = 0
            status += step

            self.channel.noiseProbability = x
            self.one_test()

            draw_data.append([self.successfullyPackage, self.repairPackage, self.badPackage, self.invisiblePackage])
            self.autoStepFinished.emit(int(status))

        self.autoStepFinished.emit(100)
        if self.is_auto:
            draw_graphic(draw_data, self.coderName, self.speed)

    def run(self):
        if self.is_auto:
            self.auto_test()
        else:
            self.one_test()

        self.stepFinished.emit(100)
        self.ended.emit()
        log.debug("Конец цикла тестов")
