# coding=utf-8
from typing import Dict, List, Optional

from PyQt5.QtCore import QThread

from src.GUI.globals_signals import globalSignals
from src.GUI.graphics import GraphicController
from src.channel.codec import Codec
from src.channel.enum_noise_mode import EnumNoiseMode
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders.abstract_coder import AbstractCoder
from src.coders.casts import int_to_bit_list
from src.coders.interleaver.Interleaver import Interleaver
from src.config.config_processor import ConfigProcessor
from src.helper.calc.simple_calculation_for_transfer_process import SimpleCalculationForTransferProcess
from src.helper.error.exception.application_exception import ApplicationException
from src.logger import log
from src.statistics.object.statistic_collector import CaseResult, TestResult, StatisticCollector
from src.statistics.object.test_result_serializer import TestResultSerializer


class SingleCoderTestThread(QThread):
    _MIN_PERCENT: float = 0.00
    _MAX_PERCENT: float = 100.00

    class GlobalTestStatistic:
        quantity_successful_package: int = 0
        quantity_error_package: int = 0
        quantity_repair_package: int = 0
        quantity_shadow_package: int = 0
        quantity_correct_bits: int = 0
        quantity_error_bits: int = 0
        based_error_bits: int = 0
        based_correct_bits: int = 0

    _information_dict: Dict = {}
    _noiseChance: float = 0
    _countTest: int = 1
    _information: int = 1
    _mode: int = 0
    _currentCoder: AbstractCoder
    _flg_auto: bool = False
    _length_interleaver: int

    _start_t: float
    _finish_t: float
    _quantity_steps: int

    # Package noise mode attr
    _noiseMode: EnumNoiseMode
    _noisePackageLength: int
    _noisePackagePeriod: int

    def __init__(
            self,
            noise_chance: float,
            count_test: int,
            test_information: int,
            current_coder: AbstractCoder,
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            noise_package_period: int,
            first_interleaver_length: Optional[int],
            start: float,
            finish: float,
            quantity_step: int,
    ):
        super(SingleCoderTestThread, self).__init__()

        self._start_t = start
        self._finish_t = finish

        self._length_interleaver = first_interleaver_length
        self._currentCoder = current_coder
        self._noiseChance = noise_chance
        self._countTest = count_test
        self._information = test_information
        self._coderSpeed = self._currentCoder.get_speed()
        self._coderName = self._currentCoder.name
        self._noiseMode = noise_mode
        self._noisePackageLength = noise_package_length
        self._noisePackagePeriod = noise_package_period
        self._quantity_steps = quantity_step

        self.channel = Codec(
            coder=self._currentCoder,
            noise_probability=self._noiseChance,
            count_cyclical=self._countTest,
            duplex=False,
            interleaver=Interleaver(first_interleaver_length) if first_interleaver_length is not None else None,
            noise_mode=noise_mode,
            noise_package_length=noise_package_length,
            noise_package_period=noise_package_period,
        )

    def __del__(self):
        self.wait()

    def set_auto(self, flag: bool) -> None:
        """
        Method provide functionality for change flag for automatic testing
        :return: None
        """
        self._flg_auto = flag

    def _single_test(self) -> TestResult:
        """
        Method provide functionality for processing single test case
        :return: TestResult
        """
        progress: float = self._MIN_PERCENT
        step: float = self._MAX_PERCENT / self._countTest
        information: list = int_to_bit_list(self._information)
        case_result_list: List[CaseResult] = []
        global_test_statistic: SingleCoderTestThread.GlobalTestStatistic = SingleCoderTestThread.GlobalTestStatistic()
        log.debug("Test cycle begin")
        for number_of_test in range(self._countTest):
            transfer_statistic: Codec.TransferStatistic = self.channel.transfer_one_step(information)
            if transfer_statistic.result_status == EnumPackageTransferResult.SUCCESS:
                global_test_statistic.quantity_successful_package += 1
            elif transfer_statistic.result_status == EnumPackageTransferResult.REPAIR:
                global_test_statistic.quantity_repair_package += 1
            elif transfer_statistic.result_status == EnumPackageTransferResult.ERROR:
                global_test_statistic.quantity_error_package += 1
            else:
                global_test_statistic.quantity_shadow_package += 1

            global_test_statistic.quantity_correct_bits += transfer_statistic.quantity_successful_bits
            global_test_statistic.quantity_error_bits += transfer_statistic.quantity_error_bits
            global_test_statistic.based_correct_bits += transfer_statistic.based_correct_bits
            global_test_statistic.based_error_bits += transfer_statistic.based_error_bits
            progress += step
            globalSignals.stepFinished.emit(int(progress))

            case_result_list.append(CaseResult(
                successfulBits=transfer_statistic.quantity_successful_bits,
                repairBits=transfer_statistic.quantity_repair_bits,
                changedBits=transfer_statistic.quantity_changed_bits,
                errorBits=transfer_statistic.quantity_error_bits
            ))

        return TestResult(
            list_case_result=case_result_list,
            first_coder=self._currentCoder,
            second_coder=None,
            noise_type=self._noiseMode,
            noise=self.channel.noiseProbability,
            flg_cascade=True,
            successful_packages=global_test_statistic.quantity_successful_package,
            repair_packages=global_test_statistic.quantity_repair_package,
            changed_packages=global_test_statistic.quantity_repair_package,
            error_packages=global_test_statistic.quantity_error_package,
            quantity_correct_bits=global_test_statistic.quantity_correct_bits,
            quantity_error_bits=global_test_statistic.quantity_error_bits,
            based_correct_bits=global_test_statistic.based_correct_bits,
            based_error_bits=global_test_statistic.based_error_bits
        )

    def _auto_test(self) -> List[TestResult]:
        log.debug("Auto-test button pressed")
        step: float = SimpleCalculationForTransferProcess.calc_noise_of_steps_different(
            start=self._start_t,
            finish=self._finish_t,
            quantity_steps=self._quantity_steps
        )
        progress: int = 0
        sum_result_of_single_test: List[TestResult] = []
        for iterator in [self._start_t + iterator * step for iterator in range(self._quantity_steps)]:
            progress += int(self._MAX_PERCENT / self._quantity_steps)
            self.channel.noiseProbability = self._MAX_PERCENT * (1 / (iterator + 1))
            sum_result_of_single_test.append(self._single_test())
            globalSignals.autoStepFinished.emit(int(progress))

        globalSignals.autoStepFinished.emit(int(self._MAX_PERCENT))
        globalSignals.autoStepFinished.emit(int(self._MAX_PERCENT))
        return sum_result_of_single_test

    def run(self):
        # noinspection PyBroadException
        try:
            if self._flg_auto:
                statistic = StatisticCollector(
                    flgCascade=False,
                    firstCoder=self._currentCoder,
                    secondCoder=None,
                    testResult=self._auto_test(),
                    lengthFirstInterleaver=self._length_interleaver,
                    lengthSecondInterleaver=None,
                    beginNoise=self._start_t,
                    endNoise=self._finish_t,
                    quantityStepsInCycle=self._quantity_steps
                )
                # Graphic should showing only for Cycle of the test
                if ConfigProcessor().config.graphic_setting.flg_enabled:
                    GraphicController().draw_graphic(statistic)
            else:
                statistic = StatisticCollector(
                    flgCascade=False,
                    firstCoder=self._currentCoder,
                    secondCoder=None,
                    testResult=[self._single_test()],
                    lengthFirstInterleaver=self._length_interleaver,
                    lengthSecondInterleaver=None,
                    beginNoise=self._start_t,
                    endNoise=self._finish_t,
                    quantityStepsInCycle=self._quantity_steps
                )

            globalSignals.stepFinished.emit(int(self._MAX_PERCENT))

            # DB Action
            if ConfigProcessor().config.db_setting.flg_used:
                TestResultSerializer().serialize_to_db(statistic)

            TestResultSerializer().serialize_to_json(statistic)
            globalSignals.ended.emit()
            log.debug("End of test cycle")

        except ApplicationException as application_exception:
            globalSignals.ended.emit()
            globalSignals.notCorrect.emit(application_exception, )
        except Exception as err:
            globalSignals.ended.emit()
            log.error(str(Exception))
            globalSignals.notCorrect.emit(ApplicationException())
