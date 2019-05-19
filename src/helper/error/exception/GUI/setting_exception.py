# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.exception.GUI.graphical_exception import GraphicalException
from src.helper.error.exception.template_exception import TemplateException


class SettingException(GraphicalException):
    _message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value
    _longMessage = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value

    INCORRECT_POLYNOMIAL: TemplateException = TemplateException(
        message="Incorrect values for _polynomial",
        long_message="""
                    Specified correct values for _polynomial.
                    Values of attribute non-changed.  
                    """
    )