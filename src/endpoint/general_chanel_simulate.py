# coding=utf-8
from typing import Optional

from src.GUI.globals_signals import globalSignals
from src.channel.enum_noise_mode import EnumNoiseMode
from src.endpoint.general_coder_simulate import GeneralCoderSimulate
from src.endpoint.thread.cascade_coder_test_thread import CascadeCoderTestThread
from src.endpoint.thread.single_coder_test_thread import SingleCoderTestThread


class GeneralChanelSimulate:
    """
    Class provide functionality for control testing process
    """
    _firstCoderParams: GeneralCoderSimulate
    _secondCoderParams: GeneralCoderSimulate

    _singleThread: SingleCoderTestThread
    _cascadeThread: CascadeCoderTestThread

    _noiseStart: float
    _noiseEnd: float
    _countTest: int
    _testInfo: int
    _mode: int

    _noiseMode: EnumNoiseMode
    _noisePackageLength: int
    _flgSplitPackage: bool
    _quantityStepsInTestCycle: int
    _packagePeriod: int

    _flgFirstInterleaver: bool
    _flgSecondInterleaver: bool
    _lengthFirstInterleaver: int
    _lengthSecondInterleaver: int

    def __init__(
            self,
            first_coder_params: Optional[GeneralCoderSimulate] = None,
            second_coder_params: Optional[GeneralCoderSimulate] = None,
            first_thread_class: Optional[SingleCoderTestThread] = None,
            cascade_thread_class: Optional[CascadeCoderTestThread] = None,
            noise_start: Optional[float] = None,
            noise_end: Optional[float] = None,
            count_test: Optional[int] = None,
            test_info: Optional[int] = None,
            mode: Optional[int] = None,
            noise_mode: Optional[EnumNoiseMode] = None,
            noise_package_length: Optional[int] = None,
            flg_split_package: Optional[bool] = None,
            quantity_steps_in_test_cycle: Optional[int] = None,
            package_period: Optional[int] = None,
            flg_first_interleaver: Optional[bool] = None,
            flg_second_interleaver: Optional[bool] = None,
            length_first_interleaver: Optional[int] = None,
            length_second_interleaver: Optional[int] = None,
    ) -> None:
        self._firstCoderParams = first_coder_params
        self._secondCoderParams = second_coder_params

        self._singleThread = first_thread_class
        self._cascadeThread = cascade_thread_class
        self._noiseStart = noise_start
        self._noiseEnd = noise_end
        self._countTest = count_test
        self._testInfo = test_info
        self._mode = mode
        self._noiseMode = noise_mode
        self._noisePackageLength = noise_package_length
        self._flgSplitPackage = flg_split_package
        self._quantityStepsInTestCycle = quantity_steps_in_test_cycle
        self._packagePeriod = package_period
        self._flgFirstInterleaver = flg_first_interleaver
        self._flgSecondInterleaver = flg_second_interleaver
        self._lengthFirstInterleaver = length_first_interleaver
        self._lengthSecondInterleaver = length_second_interleaver

    def set_first_coder_thread_class(self):
        self._singleThread = SingleCoderTestThread(
            noise_chance=self._noiseStart,
            count_test=self._countTest,
            test_information=self._testInfo,
            current_coder=self._firstCoderParams.coder,
            start=self._noiseStart,
            finish=self._noiseEnd,
            noise_package_length=self._noisePackageLength,
            noise_mode=self._noiseMode,
            noise_package_period=self._packagePeriod,
            first_interleaver_length=self._lengthFirstInterleaver if self._flgFirstInterleaver else None,
            quantity_step=self._quantityStepsInTestCycle
        )

    def set_cascade_coder_thread_class(self):
        self._cascadeThread = CascadeCoderTestThread(
            noise_chance=self._noiseStart,
            count_test=self._countTest,
            test_information=self._testInfo,
            current_coder=self._firstCoderParams.coder,
            first_coder=self._firstCoderParams.coder,
            second_coder=self._secondCoderParams.coder,
            noise_package_period=self._packagePeriod,
            noise_mode=self._noiseMode,
            noise_package_length=self._noisePackageLength,
            start=self._noiseStart,
            finish=self._noiseEnd,
            length_first_interleaver=self._lengthFirstInterleaver if self._flgFirstInterleaver else None,
            length_second_interleaver=self._lengthSecondInterleaver if self._flgSecondInterleaver else None,
            quantity_step=self._quantityStepsInTestCycle,
        )

    def start_first_single_test(self):
        globalSignals.startTesting.emit(True)
        self._firstCoderParams.create_coder()
        self.set_first_coder_thread_class()
        self._singleThread.start()

    def start_first_test_cycle(self):
        globalSignals.startTesting.emit(True)
        self._firstCoderParams.create_coder()
        self.set_first_coder_thread_class()
        self._singleThread.set_auto(True)
        self._singleThread.start()

    def start_cascade_single_test(self):
        globalSignals.startTesting.emit(True)
        self._firstCoderParams.create_coder()
        self._secondCoderParams.create_coder()
        self.set_cascade_coder_thread_class()
        self._cascadeThread.start()

    def start_cascade_test_cycle(self):
        globalSignals.startTesting.emit(True)
        self._firstCoderParams.create_coder()
        self._secondCoderParams.create_coder()
        self.set_cascade_coder_thread_class()
        self._cascadeThread.set_auto(True)
        self._cascadeThread.start()
