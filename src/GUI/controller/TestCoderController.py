import json
import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget

from src.GUI.graphics import draw_graphic, draw_plot_pie
from src.GUI.windows.TestCoderWindow import TestCoderWindow
from src.channel.channel import Channel
# noinspection PyAttributeOutsideInit
from src.coders.abstractCoder import AbstractCoder
from src.coders.casts import IntToBitList
from src.coders.exeption import CodingException
from src.coders.interleaver import Interleaver
from src.logger import log


class TestCoderController:
    _testCoderWindow: TestCoderWindow
    _mainController: None
    _lastResult: str = ""

    start: float = 1
    finish: float = 1

    def set_start(self, value):
        self.start = float(value)

    def set_finish(self, value):
        self.finish = float(value)

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
        self._threadClass = TestCoder(self._testCoderWindow, self._mainController.currentCoder, self._lastResult,
                                      start=self.start, finish=self.finish)

    def starting_test(self, param: bool):
        try:
            self.set_thread_class()
            self.enable_disable_widget(False)
            self._threadClass.set_auto(param)

            self._threadClass.autoStepFinished.connect(self._testCoderWindow.auto_test.setValue)
            self._threadClass.stepFinished.connect(self._testCoderWindow.single_test.setValue)
            self._threadClass.ended.connect(lambda: self.enable_disable_widget(True))
            self._threadClass.notCorrect.connect(self.coders_correct_warning)
            self._threadClass.start()
        except:
            QMessageBox.warning(self._testCoderWindow,
                                "Проверте параметры на корректность информации",
                                "Ошибочно заполнены поля параметров",
                                QMessageBox.Ok,
                                QMessageBox.Ok)

    def coders_correct_warning(self):
        QMessageBox.warning(self._testCoderWindow,
                            "Длина кодовых слов не согласована",
                            "Длина кодовых слов не согласована. Возможно указан слишком большой массив информации"
                            " или первый и второй кодеры не возможно поставить в каскад",
                            QMessageBox.Ok,
                            QMessageBox.Ok)
        self.enable_disable_widget(True)

    def get_last_result(self):
        msg = QMessageBox.information(self._testCoderWindow,
                                      "Последняя попытка\n",
                                      "Успешно переданно (пакет не исказился) - {0}\n"
                                      "Успешно исправленно паккетов - {1}\n"
                                      "Переданно с ошибкой - {2}\n"
                                      "Успешно битов передано - {3}\n"
                                      "Некорректные биты - {4}".
                                      format(self._threadClass.successfullyPackage,
                                             self._threadClass.repairPackage,
                                             self._threadClass.badPackage + self._threadClass.invisiblePackage,
                                             self._threadClass.countCorrectBit,
                                             self._threadClass.countErrorBit),
                                      QMessageBox.Ok | QMessageBox.Open,
                                      QMessageBox.Ok)
        if msg == QMessageBox.Open:
            os.system("lastInformation.txt")
            draw_plot_pie([self._threadClass.successfullyPackage, self._threadClass.repairPackage,
                           self._threadClass.badPackage + self._threadClass.invisiblePackage])


class TestCoder(QThread):
    TRANSFER_STR = {
        0: 'success',
        1: 'repair',
        2: 'error',
        3: 'error'
        }

    stepFinished = pyqtSignal('int')
    autoStepFinished = pyqtSignal('int')
    ended = pyqtSignal()
    notCorrect = pyqtSignal()

    information_dict = {}
    noiseChance: float = 0
    countTest: int = 1
    information: int = 1
    currentCoder: AbstractCoder
    is_auto: bool = False
    is_interleaver: bool = False
    first_length_interleaver: int = 1

    start_t: float = 0
    finish_t: float = 20

    successfullyPackage = 0
    badPackage = 0
    repairPackage = 0
    invisiblePackage = 0

    countCorrectBit = 0
    countErrorBit = 0

    def __init__(self, test_window: QWidget, currentCoder: AbstractCoder, lastResult: str,
                 start: float = 0, finish: float = 20):
        super(TestCoder, self).__init__(None)

        self.start_t = start
        self.finish_t = finish

        self.lastResult = lastResult
        self.currentCoder = currentCoder
        self.noiseChance = float(test_window.noise_text_box.text())
        self.countTest = int(test_window.count_test_text_box.text())
        self.information = int(test_window.information_text_box.text())
        self.coderSpeed = self.currentCoder.get_speed()
        self.coderName = self.currentCoder.name

        self.channel = Channel(
                self.currentCoder,
                self.noiseChance,
                self.countTest,
                False,
                Interleaver.Interleaver(int(test_window.first_length_text_box.text()))
                if test_window.is_interleaver_first.isChecked() else None)

        self.information_dict['is_cascade'] = False
        self.information_dict['coder'] = self.channel.coder.to_json()

    def __del__(self):
        self.wait()

    def set_auto(self, flag: bool):
        self.is_auto = flag

    def one_test(self) -> list:
        progress = 0.0
        step = 100.0 / self.countTest
        information: list = IntToBitList(self.information)

        log.debug("Начало цикла тестов")
        case_information = []
        for x in range(self.countTest):
            status: [int, int, int] = self.channel.transfer_one_step(information)
            if status[0] == 0:
                self.successfullyPackage += 1
            elif status[0] == 1:
                self.repairPackage += 1
            elif status[0] == 2:
                self.badPackage += 1
            else:
                self.invisiblePackage += 1
            case_information.append({x: {'correct bits': status[1], 'error bits': status[2],
                                         'status'      : self.TRANSFER_STR[status[0]]}})
            self.countCorrectBit += status[1]
            self.countErrorBit += status[2]
            progress += step
            self.lastResult += self.channel.information
            self.stepFinished.emit(int(progress))

        return case_information

    def auto_test(self):
        log.debug("Кнопка авто-тестирования нажата")
        start: float = self.start_t
        finish: float = self.finish_t

        if finish - start <= 0:
            self.notCorrect.emit()
            return
        step: float = (finish - start) / 20

        self.information_dict['auto_test_information'] = {'start': start, 'finish': finish, 'step': step}
        self.information_dict['test_cases'] = []
        draw_data: list = []  # информация для построения графика

        progress: int = 0
        for x in [start + x * step for x in range(20)]:
            test_case_info = {}

            self.successfullyPackage = 0
            self.badPackage = 0
            self.repairPackage = 0
            self.invisiblePackage = 0
            self.countErrorBit = 0
            self.countCorrectBit = 0
            progress += 5

            self.channel.noiseProbability = 100 * (1 / (x + 1))
            test_case_info['case'] = self.one_test()

            test_case_info['successfully_package_count'] = self.successfullyPackage + self.repairPackage
            test_case_info['bad_package_count'] = self.badPackage + self.invisiblePackage
            test_case_info['correct_bit_count'] = self.countCorrectBit
            test_case_info['error_bit_count'] = self.countErrorBit

            self.information_dict['test_cases'].append(test_case_info)
            draw_data.append([self.successfullyPackage, self.repairPackage, self.badPackage, self.invisiblePackage,
                              self.countCorrectBit, self.countErrorBit])
            self.autoStepFinished.emit(int(progress))

        self.information_dict['draw_information'] = draw_data
        self.autoStepFinished.emit(100)
        if self.is_auto:
            draw_graphic(self.information_dict['draw_information'],
                         self.information_dict['coder']['name'],
                         coder_speed=self.information_dict['coder']['speed'],
                         start=self.information_dict['auto_test_information']['start'],
                         finish=self.information_dict['auto_test_information']['finish'])

    def run(self):
        try:
            if self.is_auto:
                self.information_dict['single_test'] = False
                self.auto_test()
            else:
                self.information_dict['single_test'] = True
                self.information_dict['test'] = self.one_test()

            open('lastResult.json', "w", encoding='UTF-8').write(json.dumps(self.information_dict, ensure_ascii=False))
            self.stepFinished.emit(100)
            self.ended.emit()
            log.debug("Конец цикла тестов")

        except CodingException as err:
            self.notCorrect.emit()
