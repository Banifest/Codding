# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage

from src.helper.error.exception.application_exception import ApplicationException


class CoddingException(ApplicationException):
    _message = EnumExceptionStandardMessage.CODER_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.CODER_EXCEPTION.value
