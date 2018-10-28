from enum import Enum, unique


@unique
class EnumExceptionStandardMessage(Enum):
    APPLICATION_EXCEPTION = "Error occurs"
    GRAPHICAL_EXCEPTION = "Error occurs in graphical operation"
    GUI_SETTING_EXCEPTION = "Setting on GUI is incorrect"
