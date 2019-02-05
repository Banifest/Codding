# coding=utf-8
# coding=utf-8
from typing import Dict, List

from PyQt5.QtCore import QThread

from channel.enum_noise_mode import EnumNoiseMode
from src.GUI.globals_signals import globalSignals
from src.GUI.graphics import GraphicController
from src.channel.cascadecodec import CascadeCodec
from src.channel.codec import Codec
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders.abstract_coder import AbstractCoder
from src.coders.casts import int_to_bit_list
from src.helper.error.exception.codding_exception import CoddingException
from src.logger import log
from src.statistics.object.statistic_collector import CaseResult, TestResult
from src.statistics.object.test_result_serializer import TestResultSerializer


class TestCoder(QThread):
    information_dict: Dict = {}
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

    # Package noise mode attr
    noiseMode: EnumNoiseMode
    noisePackageLength: int
    isSplitPackage: bool

    def __init__(
            self,
            noise_chance: float,
            count_test: float,
            test_info: int,
            current_coder: AbstractCoder,
            last_result: str,
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            is_split_package: bool,
            start: float = 0,
            finish: float = 20,
    ):
        super(TestCoder, self).__init__()

        self.start_t = start
        self.finish_t = finish

        self.lastResult = last_result
        self.currentCoder = current_coder
        self.noiseChance = noise_chance
        self.countTest = count_test
        self.information = test_info
        self.coderSpeed = self.currentCoder.get_speed()
        self.coderName = self.currentCoder.name
        self.noiseMode = noise_mode
        self.noisePackageLength = noise_package_length
        self.isSplitPackage = is_split_package

        self.channel = Codec(
            self.currentCoder,
            self.noiseChance,
            self.countTest,
            False,
            None,
            noise_mode=noise_mode,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
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
        progress: float = 0.0
        step: float = 100.0 / self.countTest
        information: list = int_to_bit_list(self.information)
        case_result_list: List[CaseResult] = []

        log.debug("Начало цикла тестов")
        case_information: list = []
        for x in range(self.countTest):
            transfer_statistic: Codec.TransferStatistic = self.channel.transfer_one_step(information)
            if transfer_statistic.result_status == EnumPackageTransferResult.SUCCESS:
                self.successfullyPackage += 1
            elif transfer_statistic.result_status == EnumPackageTransferResult.REPAIR:
                self.repairPackage += 1
            elif transfer_statistic.result_status == EnumPackageTransferResult.ERROR:
                self.badPackage += 1
            else:
                self.invisiblePackage += 1
            case_information.append({
                x: {
                    'correct bits': transfer_statistic.quantity_successful_bits,
                    'error bits': transfer_statistic.quantity_error_bits,
                    'repair bits': transfer_statistic.quantity_repair_bits,
                    'change bits': transfer_statistic.quantity_changed_bits,
                    'status': transfer_statistic.result_status.value
                }
            })
            self.countCorrectBit += transfer_statistic.quantity_successful_bits
            self.countErrorBit += transfer_statistic.quantity_error_bits
            progress += step
            self.lastResult += self.channel.information
            globalSignals.stepFinished.emit(int(progress))

            case_result_list.append(CaseResult(
                successful_bits=transfer_statistic.quantity_successful_bits,
                repair_bits=transfer_statistic.quantity_repair_bits,
                changed_bits=transfer_statistic.quantity_changed_bits,
                error_bits=transfer_statistic.quantity_error_bits
            ))

        TestResult(
            list_case_result=case_result_list,
            first_coder=self.currentCoder,
            second_coder=None,
            noise_type=self.noiseMode,
            noise=self.channel.noiseProbability,
            flg_cascade=True
        )

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
            GraphicController().draw_graphic(
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

        except CoddingException:
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
