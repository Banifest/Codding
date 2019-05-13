# coding=utf-8
from enum import Enum, unique


@unique
class EnumExceptionStandardMessage(Enum):
    APPLICATION_EXCEPTION = "Error occurs"
    GRAPHICAL_EXCEPTION = "Error occurs in graphical interface"
    GUI_SETTING_EXCEPTION = "Setting on GUI is incorrect"
    PARAMETERS_PARSE_CONSOLE_EXCEPTION = "Error occurs then parse parameters"
    CODER_EXCEPTION = "Unknown exception with coder"
