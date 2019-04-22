# coding=utf-8
from numpy import deprecate

from src.GUI.controller.coder_controller import CoderController
from src.channel.enum_noise_mode import EnumNoiseMode
from src.endpoint.general_chanel_simulate import GeneralChanelSimulate
from src.helper.error.error_handler import ErrorHandler
from src.helper.error.exception.application_exception import ApplicationException
from src.helper.error.exception.parameters_parse_exception import ParametersParseException


class TestController(GeneralChanelSimulate):
    """
    Class provide functionality for control testing process
    """
    _NOISE_MIN: int = 1
    _NOISE_MAX: int = 50

    def __init__(
            self,
            first_coder_params: CoderController,
            second_coder_params: CoderController,
    ):
        super().__init__(
            first_coder_params=first_coder_params,
            second_coder_params=second_coder_params,
        )
        # Should be defined
        self._noiseStart = self._NOISE_MIN
        self._noiseEnd = self._NOISE_MAX

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

    def set_noise_package_period(self, value: int) -> None:
        if value <= self._noisePackageLength:
            pass
        else:
            self._packagePeriod = value

    def set_noise_single_mode(self, value: bool) -> None:
        if value:
            self._noiseMode = EnumNoiseMode.SINGLE

    def set_noise_package_mode(self, value: bool) -> None:
        if value:
            self._noiseMode = EnumNoiseMode.PACKAGE

    def set_noise_mix_mode(self, value: bool) -> None:
        if value:
            self._noiseMode = EnumNoiseMode.MIX

    def set_noise_package_length(self, value: int) -> None:
        self._noisePackageLength = value

    def set_is_split_package(self, value: bool) -> None:
        self._flgSplitPackage = value

    def set_noise_start(self, value: float) -> None:
        if value > self._noiseEnd:
            ErrorHandler().gui_message_box(
                rcx_exception=ParametersParseException(
                    message=ParametersParseException.START_NOISE_LE_END.message,
                    long_message=ParametersParseException.START_NOISE_LE_END.long_message,
                )
            )
        else:
            self._noiseStart = value

    def set_noise_end(self, value: float) -> None:
        if value < self._noiseStart:
            ErrorHandler().gui_message_box(
                rcx_exception=ParametersParseException(
                    message=ParametersParseException.START_NOISE_LE_END.message,
                    long_message=ParametersParseException.START_NOISE_LE_END.long_message,
                )
            )
        else:
            self._noiseEnd = value

    def set_count_test(self, value: int) -> None:
        self._countTest = value

    def set_test_info(self, value: str) -> None:
        try:
            self._testInfo = int(value)
        except ValueError as rcx_value_error:
            ErrorHandler().gui_message_box(
                rcx_exception=ParametersParseException(
                    message=ParametersParseException.INFORMATION_NOT_SERIALIZABLE.message,
                    long_message=ParametersParseException.INFORMATION_NOT_SERIALIZABLE.long_message,
                    previous=rcx_value_error
                )
            )

    @deprecate
    def set_mode_cascade(self, value: str) -> None:
        if value == 'First':
            self._mode = 0
        elif value == 'Second':
            self._mode = 1

    def start_first_single_test(self):
        try:
            super().start_first_single_test()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)

    def start_first_test_cycle(self):
        try:
            super().start_first_test_cycle()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)

    def start_cascade_single_test(self):
        try:
            super().start_cascade_single_test()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)

    def start_cascade_test_cycle(self):
        try:
            super().start_cascade_test_cycle()
        except ApplicationException as rcx_app_exception:
            ErrorHandler().gui_message_box(rcx_exception=rcx_app_exception)
