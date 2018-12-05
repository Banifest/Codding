# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.exception.application_exception import ApplicationException


class ParametersParseException(ApplicationException):
    _message = EnumExceptionStandardMessage.PARAMETERS_PARSE_CONSOLE_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.PARAMETERS_PARSE_CONSOLE_EXCEPTION.value
