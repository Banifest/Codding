# coding=utf-8
# coding=utf-8

from channel.enum_noise_mode import EnumNoiseMode
from src.GUI.controller.coder_controller import CoderController
from src.GUI.controller.thread_controllers import TestCoder, TestCascadeCoder
from src.helper.error.error_handler import ErrorHandler
from src.helper.error.exception.application_exception import ApplicationException


class TestController:
    """
    Class provide functionality for control testing process
    """
    _firstCoderParams: CoderController
    _secondCoderParams: CoderController

    _firstThreadClass: TestCoder
    _cascadeThreadClass: TestCascadeCoder

    # TODO Why not constant?
    noiseStart: float = 1.0
    noiseEnd: float = 10.0
    countTest: int = 100
    testInfo: int = 985
    mode: int = 0

    noiseMode: EnumNoiseMode
    noisePackageLength: int
    isSplitPackage: bool

    def __init__(
            self,
            first_coder_params: CoderController,
            second_coder_params: CoderController,
    ):
        self._firstCoderParams = first_coder_params
        self._secondCoderParams = second_coder_params

    def set_noise_mode(self, value: bool) -> None:
        if value:
            self.noiseMode = EnumNoiseMode.SINGLE
        else:
            self.noiseMode = EnumNoiseMode.PACKAGE

    def set_noise_package_length(self, value: int) -> None:
        self.noisePackageLength = value

    def set_is_split_package(self, value: bool) -> None:
        self.isSplitPackage = value

    def set_noise_start(self, value: float) -> None:
        self.noiseStart = value

    def set_noise_end(self, value: float) -> None:
        self.noiseEnd = value

    def set_count_test(self, value: int) -> None:
        self.countTest = value

    def set_test_info(self, value: int) -> None:
        try:
            self.testInfo = int(value)
        except ValueError as rcx_value_error:
            pass

    def set_mode_cascade(self, value: str) -> None:
        if value == 'First':
            self.mode = 0
        elif value == 'Second':
            self.mode = 1

    def set_first_coder_thread_class(self):
        self._firstThreadClass = TestCoder(
            noise_chance=self.noiseStart,
            count_test=self.countTest,
            test_info=self.testInfo,
            current_coder=self._firstCoderParams.coder,
            last_result='',
            start=self.noiseStart,
            finish=self.noiseEnd
        )

    def set_cascade_coder_thread_class(self):
        self._cascadeThreadClass = TestCascadeCoder(
            noise_chance=self.noiseStart,
            count_test=self.countTest,
            test_info=self.testInfo,
            current_coder=self._firstCoderParams.coder,
            first_coder=self._firstCoderParams.coder,
            second_coder=self._secondCoderParams.coder,
            last_result='',
            start=self.noiseStart,
            finish=self.noiseEnd,
            mode=self.mode
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
