# coding=utf-8
from src.endpoint.general_coder_simulate import GeneralCoderSimulate
from src.helper.error.error_handler import ErrorHandler
from src.helper.error.exception.GUI.setting_exception import SettingException


class CoderController(GeneralCoderSimulate):
    def __init__(self):
        super().__init__()

    def set_coder_type(self, value: int) -> None:
        self._coderTypeInt = value

    def set_hem_size_pack(self, value: int) -> None:
        self._hemSizePack = value

    def set_cyc_size_pack(self, value: int) -> None:
        self._cycSizePack = value

    def set_cyc_poly(self, value: int) -> None:
        self._cycPoly = value

    def set_con_list_poly(self, value: str) -> None:
        self._conListPoly = value

    def set_con_count_reg(self, value: int) -> None:
        self._conCountReg = value

    def set_fou_size_pack(self, value: int) -> None:
        self._fouSizePack = value

    def set_fou_size_block(self, value: int) -> None:
        self._fouSizeBlock = value

    def set_fou_count_block(self, value: int) -> None:
        self._fouCountBlock = value

    def create_coder(self):
        try:
            super().create_coder()
        except SettingException as rcx_setting:
            ErrorHandler.gui_message_box(rcx_exception=rcx_setting)
