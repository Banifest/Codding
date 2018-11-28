# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.error_handler import ErrorHandler
from src.helper.error.exception.application_exception import ApplicationException


class GraphicalException(ApplicationException):
    _message = EnumExceptionStandardMessage.GRAPHICAL_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.GRAPHICAL_EXCEPTION.value

    def show_message_box(self):
        ErrorHandler().gui_message_box(rcx_exception=self)
