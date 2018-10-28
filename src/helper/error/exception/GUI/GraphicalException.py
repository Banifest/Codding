from src.helper.error.EnumExceptionStandardMessage import EnumExceptionStandardMessage
from src.helper.error.ErrorHandler import ErrorHandler
from src.helper.error.exception.ApplicationException import ApplicationException


class GraphicalException(ApplicationException):
    _message = EnumExceptionStandardMessage.GRAPHICAL_EXCEPTION
    _long_message = EnumExceptionStandardMessage.GRAPHICAL_EXCEPTION

    def show_message_box(self):
        ErrorHandler().gui_message_box(rcx_exception=self)
