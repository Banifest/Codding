# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.exception.GUI.graphical_exception import GraphicalException
from src.helper.error.exception.template_exception import TemplateException


class SettingException(GraphicalException):
    _message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.GUI_SETTING_EXCEPTION.value

    INCORRECT_POLYNOMIAL: TemplateException = TemplateException(
        message="Incorrect values for polynomial",
        long_message="""
                    Specified correct values for polynomial.
                    Values of attribute non-changed.  
                    """
    )