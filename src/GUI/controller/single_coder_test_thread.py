# coding=utf-8
# coding=utf-8
from typing import Dict, List, Optional

from PyQt5.QtCore import QThread

from src.GUI.globals_signals import globalSignals
from src.channel.codec import Codec
from src.channel.enum_noise_mode import EnumNoiseMode
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders.abstract_coder import AbstractCoder
from src.coders.casts import int_to_bit_list
from src.coders.interleaver.Interleaver import Interleaver
from src.helper.error.exception.codding_exception import CoddingException
from src.logger import log
from src.statistics.object.statistic_collector import CaseResult, TestResult, StatisticCollector
from src.statistics.object.test_result_serializer import TestResultSerializer


class SingleCoderTestThread(QThread):
    CONST_MIN_PERCENT: float = 0.00
    CONST_MAX_PERCENT: float = 100.00

    class GlobalTestStatistic:
        quantity_successful_package: int = 0
        quantity_error_package: int = 0
        quantity_repair_package: int = 0
        quantity_shadow_package: int = 0
        quantity_correct_bits: int = 0
        quantity_error_bits: int = 0

    _information_dict: Dict = {}
    _noiseChance: float = 0
    _countTest: int = 1
    _information: int = 1
    _mode: int = 0
    _currentCoder: AbstractCoder
    _flg_auto: bool = False

    _start_t: float = 0
    _finish_t: float = 20

    globalTestStatistic: GlobalTestStatistic = GlobalTestStatistic()

    # Package noise mode attr
    _noiseMode: EnumNoiseMode
    _noisePackageLength: int
    _isSplitPackage: bool

    _sum_result_of_single_test: List[TestResult] = []

    def __init__(
            self,
            noise_chance: float,
            count_test: float,
            test_information: int,
            current_coder: AbstractCoder,
            last_result: str,
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            is_split_package: bool,
            first_interleaver_length: Optional[int],
            start: float = 0,
            finish: float = 20,
    ):
        super(SingleCoderTestThread, self).__init__()

        self._start_t = start
        self._finish_t = finish

        self.lastResult = last_result
        self._currentCoder = current_coder
        self._noiseChance = noise_chance
        self._countTest = count_test
        self._information = test_information
        self._coderSpeed = self._currentCoder.get_speed()
        self._coderName = self._currentCoder.name
        self._noiseMode = noise_mode
        self._noisePackageLength = noise_package_length
        self._isSplitPackage = is_split_package

        self.channel = Codec(
            coder=self._currentCoder,
            noise_probability=self._noiseChance,
            count_cyclical=self._countTest,
            duplex=False,
            interleaver=Interleaver(first_interleaver_length) if first_interleaver_length is not None else None,
            noise_mode=noise_mode,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
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
        :return:
        """
        progress: float = self.CONST_MIN_PERCENT
        step: float = self.CONST_MAX_PERCENT / self._countTest
        information: list = int_to_bit_list(self._information)
        case_result_list: List[CaseResult] = []

        log.debug("Начало цикла тестов")
        for x in range(self._countTest):
            transfer_statistic: Codec.TransferStatistic = self.channel.transfer_one_step(information)
            if transfer_statistic.result_status == EnumPackageTransferResult.SUCCESS:
                self.globalTestStatistic.quantity_successful_package += 1
            elif transfer_statistic.result_status == EnumPackageTransferResult.REPAIR:
                self.globalTestStatistic.quantity_repair_package += 1
            elif transfer_statistic.result_status == EnumPackageTransferResult.ERROR:
                self.globalTestStatistic.quantity_error_package += 1
            else:
                self.globalTestStatistic.quantity_shadow_package += 1

            self.globalTestStatistic.quantity_correct_bits += transfer_statistic.quantity_successful_bits
            self.globalTestStatistic.quantity_error_bits += transfer_statistic.quantity_error_bits
            progress += step
            self.lastResult += self.channel.information
            globalSignals.stepFinished.emit(int(progress))

            case_result_list.append(CaseResult(
                successful_bits=transfer_statistic.quantity_successful_bits,
                repair_bits=transfer_statistic.quantity_repair_bits,
                changed_bits=transfer_statistic.quantity_changed_bits,
                error_bits=transfer_statistic.quantity_error_bits
            ))

        return TestResult(
            list_case_result=case_result_list,
            first_coder=self._currentCoder,
            second_coder=None,
            noise_type=self._noiseMode,
            noise=self.channel.noiseProbability,
            flg_cascade=True
        )

    def _auto_test(self) -> List[TestResult]:
        log.debug("Кнопка авто-тестирования нажата")
        start: float = self._start_t
        finish: float = self._finish_t

        if finish - start <= 0:
            globalSignals.notCorrect.emit()
        step: float = (finish - start) / 20
        progress: int = 0

        for iterator in [start + iterator * step for iterator in range(20)]:
            progress += 5
            self.channel.noiseProbability = 100 * (1 / (iterator + 1))
            self._sum_result_of_single_test.append(self._single_test())
            globalSignals.autoStepFinished.emit(int(progress))

        globalSignals.autoStepFinished.emit(100)
        return self._sum_result_of_single_test

    def run(self):
        try:
            if self._flg_auto:
                statistic = StatisticCollector(
                    flg_cascade=False,
                    first_coder=self._currentCoder,
                    second_coder=None,
                    test_result=self._auto_test()
                )
            else:
                statistic = StatisticCollector(
                    flg_cascade=False,
                    first_coder=self._currentCoder,
                    second_coder=None,
                    test_result=[self._single_test()]
                )

            globalSignals.stepFinished.emit(100)
            globalSignals.ended.emit()

            # DB Action
            TestResultSerializer().serialize_to_db(statistic)
            log.debug("Конец цикла тестов")

        except CoddingException:
            globalSignals.notCorrect.emit()
