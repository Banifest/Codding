# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.exception.GUI.GraphicalException import GraphicalException


class SettingException(GraphicalException):
    _message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value
