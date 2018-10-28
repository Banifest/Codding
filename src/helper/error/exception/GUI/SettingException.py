from src.helper.error.EnumExceptionStandardMessage import EnumExceptionStandardMessage
from src.helper.error.exception.GUI.GraphicalException import GraphicalException


class SettingException(GraphicalException):
    _message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value
