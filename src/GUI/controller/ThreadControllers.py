# coding=utf-8
# coding=utf-8

from PyQt5.QtCore import QThread

from src.GUI.globals_signals import globalSignals
from src.GUI.graphics import draw_graphic
from src.channel.cascadecodec import CascadeCodec
from src.channel.codec import Codec
from src.coders.abstract_coder import AbstractCoder
from src.coders.casts import IntToBitList
from src.coders.exeption import CodingException
from src.logger import log
from src.statistics.object.test_result_serializer import TestResultSerializer


class TestCoder(QThread):
    TRANSFER_STR = {
        0: 'success',
        1: 'repair',
        2: 'error',
        3: 'error'
    }

    information_dict = {}
    noiseChance: float = 0
    countTest: int = 1
    information: int = 1
    mode: int = 0
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

        self.channel = Codec(
            self.currentCoder,
            self.noiseChance,
            self.countTest,
            False,
            None
        )

        self.information_dict['is_cascade'] = False
        self.information_dict['coder'] = self.channel.coder.to_json()

    def __del__(self):
        self.wait()

    def set_auto(self, flag: bool):
        """
        Method provide functionality for change flag for automatic
        :return:
        """
        self.is_auto = flag

    def one_test(self) -> list:
        """
        Method provide functionality for processing single test case
        :return:
        """
        progress = 0.0
        step = 100.0 / self.countTest
        information: list = IntToBitList(self.information)

        log.debug("Начало цикла тестов")
        case_information = []
        for x in range(self.countTest):
            status: [int, int, int, int, int] = self.channel.transfer_one_step(information)
            if status[0] == 0:
                self.successfullyPackage += 1
            elif status[0] == 1:
                self.repairPackage += 1
            elif status[0] == 2:
                self.badPackage += 1
            else:
                self.invisiblePackage += 1
            case_information.append({
                x: {
                    'correct bits': status[1],
                    'error bits': status[2],
                    'repair bits': status[3],
                    'change bits': status[4],
                    'status': self.TRANSFER_STR[status[0]]
                }
            })
            self.countCorrectBit += status[1]
            self.countErrorBit += status[2]
            progress += step
            self.lastResult += self.channel.information
            globalSignals.stepFinished.emit(int(progress))

        return case_information

    def auto_test(self):
        log.debug("Кнопка авто-тестирования нажата")
        start: float = self.start_t
        finish: float = self.finish_t

        if finish - start <= 0:
            globalSignals.notCorrect.emit()
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
            globalSignals.autoStepFinished.emit(int(progress))

        self.information_dict['draw_information'] = draw_data
        globalSignals.autoStepFinished.emit(100)
        if self.is_auto:
            draw_graphic(
                self.information_dict['draw_information'],
                self.information_dict['coder']['name'],
                coder_speed=self.information_dict['coder']['speed'],
                start=self.information_dict['auto_test_information']['start'],
                finish=self.information_dict['auto_test_information']['finish']
            )

    def run(self):
        try:
            if self.is_auto:
                self.information_dict['single_test'] = False
                self.auto_test()
            else:
                self.information_dict['single_test'] = True
                self.information_dict['test'] = self.one_test()

            # Сохраненение в JSON
            TestResultSerializer().serialize_to_json(self.information_dict)
            # Созранение в базе данных
            if not self.information_dict['is_cascade']:
                TestResultSerializer().serialize_to_db(self.information_dict, self.currentCoder)

            globalSignals.stepFinished.emit(100)
            globalSignals.ended.emit()
            log.debug("Конец цикла тестов")

        except CodingException as err:
            globalSignals.notCorrect.emit()


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
                 finish: float = 20,
                 mode: int = 0
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
        self.channel = CascadeCodec(
            first_coder,
            second_coder,
            self.noiseChance,
            self.countTest,
            False,
            None,
            None,
            mode
        )

    def run(self):
        self.information_dict['is_cascade'] = True
        self.information_dict['coder'] = {
            'first_coder': self.channel.firstCoder.to_json(),
            'second_coder': self.channel.secondCoder.to_json(),
            'name': self.coderName,
            'speed': self.coderSpeed
        }
        super().run()
        if self.information_dict['is_cascade']:
            TestResultSerializer().serialize_to_db(
                self.information_dict,
                self.channel.firstCoder,
                self.channel.secondCoder
            )
