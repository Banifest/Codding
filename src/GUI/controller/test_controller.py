# coding=utf-8
# coding=utf-8

from src.GUI.controller.cascade_coder_test_thread import CascadeCoderTestThread
from src.GUI.controller.coder_controller import CoderController
from src.GUI.controller.single_coder_test_thread import SingleCoderTestThread
from src.channel.enum_noise_mode import EnumNoiseMode
from src.helper.error.error_handler import ErrorHandler
from src.helper.error.exception.application_exception import ApplicationException


class TestController:
    """
    Class provide functionality for control testing process
    """
    _firstCoderParams: CoderController
    _secondCoderParams: CoderController

    _firstThreadClass: SingleCoderTestThread
    _cascadeThreadClass: CascadeCoderTestThread

    _noiseStart: float
    _noiseEnd: float
    _countTest: int
    _testInfo: int
    _mode: int

    _noiseMode: EnumNoiseMode
    _noisePackageLength: int
    _flgSplitPackage: bool
    _quantityStepsInTestCycle: int

    _flgFirstInterleaver: bool
    _flgSecondInterleaver: bool
    _lengthFirstInterleaver: int
    _lengthSecondInterleaver: int

    def __init__(
            self,
            first_coder_params: CoderController,
            second_coder_params: CoderController,
    ):
        self._firstCoderParams = first_coder_params
        self._secondCoderParams = second_coder_params

    def set_quantity_steps_in_test_cycle(self, value: int) -> None:
        self._quantityStepsInTestCycle = value

    def set_flg_first_interleaver(self, value: bool) -> None:
        self._flgFirstInterleaver = value

    def set_flg_second_interleaver(self, value: bool) -> None:
        self._flgSecondInterleaver = value

    def set_length_first_interleaver(self, value: int) -> None:
        self._lengthFirstInterleaver = value

    def set_length_second_interleaver(self, value: int) -> None:
        self._lengthSecondInterleaver = value

    def set_noise_mode(self, value: bool) -> None:
        if value:
            self._noiseMode = EnumNoiseMode.SINGLE
        else:
            self._noiseMode = EnumNoiseMode.PACKAGE

    def set_noise_package_length(self, value: int) -> None:
        self._noisePackageLength = value

    def set_is_split_package(self, value: bool) -> None:
        self._flgSplitPackage = value

    def set_noise_start(self, value: float) -> None:
        self._noiseStart = value

    def set_noise_end(self, value: float) -> None:
        self._noiseEnd = value

    def set_count_test(self, value: int) -> None:
        self._countTest = value

    def set_test_info(self, value: int) -> None:
        try:
            self._testInfo = int(value)
        except ValueError as rcx_value_error:
            pass

    def set_mode_cascade(self, value: str) -> None:
        if value == 'First':
            self._mode = 0
        elif value == 'Second':
            self._mode = 1

    def set_first_coder_thread_class(self):
        self._firstThreadClass = SingleCoderTestThread(
            noise_chance=self._noiseStart,
            count_test=self._countTest,
            test_information=self._testInfo,
            current_coder=self._firstCoderParams.coder,
            start=self._noiseStart,
            finish=self._noiseEnd,
            noise_package_length=self._noisePackageLength,
            noise_mode=self._noiseMode,
            is_split_package=self._flgSplitPackage,
            first_interleaver_length=self._lengthFirstInterleaver if self._flgFirstInterleaver else None,
            quantity_step=self._quantityStepsInTestCycle
        )

    def set_cascade_coder_thread_class(self):
        self._cascadeThreadClass = CascadeCoderTestThread(
            noise_chance=self._noiseStart,
            count_test=self._countTest,
            test_information=self._testInfo,
            current_coder=self._firstCoderParams.coder,
            first_coder=self._firstCoderParams.coder,
            second_coder=self._secondCoderParams.coder,
            is_split_package=self._flgSplitPackage,
            noise_mode=self._noiseMode,
            noise_package_length=self._noisePackageLength,
            start=self._noiseStart,
            finish=self._noiseEnd,
            length_first_interleaver=self._lengthFirstInterleaver if self._flgFirstInterleaver else None,
            length_second_interleaver=self._lengthSecondInterleaver if self._flgSecondInterleaver else None,
            quantity_step=self._quantityStepsInTestCycle,
        )

    def start_first_single_test(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_first_coder_thread_class()
            self._firstThreadClass.start()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)

    def start_first_test_cycle(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_first_coder_thread_class()
            self._firstThreadClass.set_auto(True)
            self._firstThreadClass.start()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)

    def start_cascade_single_test(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_cascade_coder_thread_class()
            self._cascadeThreadClass.start()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)

    def start_cascade_test_cycle(self):
        self._firstCoderParams.create_coder()
        self._secondCoderParams.create_coder()
        try:
            self.set_cascade_coder_thread_class()
            self._cascadeThreadClass.set_auto(True)
            self._cascadeThreadClass.start()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)
