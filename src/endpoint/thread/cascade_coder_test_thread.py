# coding=utf-8
from typing import Optional

from src.GUI.globals_signals import globalSignals
from src.GUI.graphics import GraphicController
from src.channel.cascadecodec import CascadeCodec
from src.channel.enum_noise_mode import EnumNoiseMode
from src.coders.abstract_coder import AbstractCoder
from src.coders.interleaver.Interleaver import Interleaver
from src.config.config_processor import ConfigProcessor
from src.endpoint.thread.single_coder_test_thread import SingleCoderTestThread
from src.helper.error.exception.codding_exception import CodingException
from src.logger import log
from src.statistics.object.statistic_collector import StatisticCollector
from src.statistics.object.test_result_serializer import TestResultSerializer


class CascadeCoderTestThread(SingleCoderTestThread):
    _firstCoder: AbstractCoder
    _secondCoder: AbstractCoder

    _length_first_interleaver: Optional[int]
    _length_second_interleaver: Optional[int]

    def __init__(
            self,
            noise_chance: float,
            count_test: int,
            test_information: int,
            current_coder: AbstractCoder,
            first_coder: AbstractCoder,
            second_coder: AbstractCoder,
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            noise_package_period: int,
            length_first_interleaver: Optional[int],
            length_second_interleaver: Optional[int],
            start: float,
            finish: float,
            quantity_step: int,
    ):
        super().__init__(
            noise_chance=noise_chance,
            count_test=count_test,
            test_information=test_information,
            current_coder=current_coder,
            start=start,
            finish=finish,
            noise_package_length=noise_package_length,
            noise_package_period=noise_package_period,
            noise_mode=noise_mode,
            first_interleaver_length=length_first_interleaver,
            quantity_step=quantity_step
        )

        self._length_first_interleaver = length_first_interleaver
        self._length_second_interleaver = length_first_interleaver

        self._firstCoder = first_coder
        self._secondCoder = second_coder
        self.coderSpeed = first_coder.get_speed() * second_coder.get_speed()
        self.coderName = 'Cascade codec: {0} and {1}'.format(first_coder.name, second_coder.name)
        self.channel = CascadeCodec(
            first_coder=first_coder,
            second_coder=second_coder,
            noise_probability=self._noiseChance,
            count_cyclical=self._countTest,
            duplex=False,
            first_interleaver=Interleaver(length_first_interleaver
                                          ) if length_first_interleaver is not None else None,
            second_interleaver=Interleaver(length_second_interleaver
                                           ) if length_second_interleaver is not None else None,
            noise_package_length=noise_package_length,
            noise_package_period=noise_package_period,
            noise_mode=noise_mode,
        )

    def run(self):
        try:
            if self._flg_auto:
                statistic = StatisticCollector(
                    flgCascade=True,
                    firstCoder=self._firstCoder,
                    secondCoder=self._secondCoder,
                    testResult=self._auto_test(),
                    lengthFirstInterleaver=self._length_first_interleaver,
                    lengthSecondInterleaver=self._length_second_interleaver,
                    beginNoise=self._start_t,
                    endNoise=self._finish_t,
                    quantityStepsInCycle=self._quantity_steps
                )

                if ConfigProcessor().config.graphic_setting.flg_enabled:
                    GraphicController().draw_graphic(statistic)
            else:
                statistic = StatisticCollector(
                    flgCascade=True,
                    firstCoder=self._firstCoder,
                    secondCoder=self._secondCoder,
                    testResult=[self._single_test()],
                    lengthFirstInterleaver=self._length_first_interleaver,
                    lengthSecondInterleaver=self._length_second_interleaver,
                    beginNoise=self._start_t,
                    endNoise=self._finish_t,
                    quantityStepsInCycle=self._quantity_steps
                )

            globalSignals.stepFinished.emit(int(self._MAX_PERCENT))
            globalSignals.ended.emit()

            # DB Action
            if ConfigProcessor().config.db_setting.flg_used:
                TestResultSerializer().serialize_to_db(statistic)
            TestResultSerializer().serialize_to_json(statistic)

            log.debug("End of the test cycle")

        except CodingException as coddingException:
            globalSignals.notCorrect.emit(coddingException)
