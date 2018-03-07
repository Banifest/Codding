import json

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QProgressBar, QWidget

from src.GUI.controller import CoderController
from src.GUI.graphics import draw_graphic
from src.channel.cascade import Cascade
from src.channel.channel import Channel
from src.coders.abstractCoder import AbstractCoder
from src.coders.casts import IntToBitList
from src.coders.exeption import CodingException
from src.coders.interleaver.Interleaver import Interleaver
from src.logger import log

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

    def __init__(self,
                 noise_chance: float,
                 count_test: float,
                 test_info: int,
                 current_coder: AbstractCoder,
                 last_result: str,
                 start: float = 0,
                 finish: float = 20):
        super(TestCoder, self).__init__(None)

        self.start_t = start
        self.finish_t = finish

        self.lastResult = last_result
        self.currentCoder = current_coder
        self.noiseChance = noise_chance
        self.countTest = count_test
        self.information = test_info
        self.coderSpeed = self.currentCoder.get_speed()
        self.coderName = self.currentCoder.name

        self.channel = Channel(
                self.currentCoder,
                self.noiseChance,
                self.countTest,
                False,
                None)

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
            case_information.append({x: {'correct bits': status[1],
                                         'error bits': status[2],
                                         'status': self.TRANSFER_STR[status[0]]}})
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


class TestCascadeCoder(TestCoder):
    def __init__(self,
                 noise_chance: float,
                 count_test: float,
                 test_info: int,
                 current_coder: AbstractCoder,
                 first_coder: AbstractCoder,
                 second_coder: AbstractCoder,
                 last_result: str,
                 start: float = 0,
                 finish: float = 20
                 ):
        super().__init__(noise_chance,
                         count_test,
                         test_info,
                         current_coder,
                         last_result,
                         start,
                         finish)

        self.coderSpeed = first_coder.get_speed() * second_coder.get_speed()
        self.coderName = 'Каскадный кодер из: {0} и {1}'.format(first_coder.name, second_coder.name)
        self.channel = Cascade(
                first_coder,
                second_coder,
                self.noiseChance,
                self.countTest,
                False,
                None,
                None)

    def run(self):
        self.information_dict['is_cascade'] = True
        super().run()
        self.information_dict['coder'] = {
            'first_coder': self.channel.firstCoder.to_json(),
            'second_coder': self.channel.secondCoder.to_json(),
            'name': self.coderName,
            'speed': self.coderSpeed
        }


class TestController:
    _firstCoderParams: CoderController
    _secondCoderParams: CoderController

    _firstThreadClass: TestCoder
    _cascadeThreadClass: TestCascadeCoder

    _singleProgress: QProgressBar
    _autoProgress: QProgressBar

    noiseStart: float = 1.0
    noiseEnd: float = 2.0
    countTest: int = 100
    testInfo: int = 985

    _test_type: int = 0

    def __init__(self,
                 first_coder_params: CoderController,
                 second_coder_params: CoderController,
                 ):
        self._firstCoderParams = first_coder_params
        self._secondCoderParams = second_coder_params

    def set_single_progress(self, single_progress: QProgressBar) -> None:
        self._singleProgress = single_progress

    def set_auto_progress(self, auto_progress: QProgressBar) -> None:
        self._autoProgress = auto_progress

    def set_noise_start(self, value: float) -> None:
        self.noiseStart = value

    def set_noise_end(self, value: float) -> None:
        self.noiseEnd = value

    def set_count_test(self, value: int) -> None:
        self.countTest = value

    def set_test_info(self, value: int) -> None:
        self.testInfo = value

    def set_first_coder_thread_class(self):
        self._firstThreadClass = TestCoder(self.noiseStart,
                                           self.countTest,
                                           self.testInfo,
                                           self._firstCoderParams.coder,
                                           '',
                                           start=self.noiseStart,
                                           finish=self.noiseEnd)

    def set_cascade_coder_thread_class(self):
        self._cascadeThreadClass = TestCascadeCoder(
                self.noiseStart,
                self.countTest,
                self.testInfo,
                self._firstCoderParams.coder,
                self._firstCoderParams.coder,
                self._secondCoderParams.coder,
                '',
                self.noiseStart,
                self.noiseEnd
        )

    def start_first_single_test(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_first_coder_thread_class()
            self._firstThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._firstThreadClass.start()
        except:
            pass

    def start_first_test_cycle(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_first_coder_thread_class()
            self._firstThreadClass.set_auto(True)
            self._firstThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._firstThreadClass.autoStepFinished.connect(self._autoProgress.setValue)
            self._firstThreadClass.start()
        except:
            pass

    def start_cascade_single_test(self):
        self._firstCoderParams.create_coder()
        self._secondCoderParams.create_coder()
        try:
            self.set_cascade_coder_thread_class()
            self._cascadeThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._cascadeThreadClass.start()
        except:
            pass

    def start_cascade_test_cycle(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_cascade_coder_thread_class()
            self._cascadeThreadClass.set_auto(True)
            self._cascadeThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._cascadeThreadClass.autoStepFinished.connect(self._autoProgress.setValue)
            self._cascadeThreadClass.start()
        except:
            pass
