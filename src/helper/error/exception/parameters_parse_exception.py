# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.exception.application_exception import ApplicationException
from src.helper.error.exception.template_exception import TemplateException


class ParametersParseException(ApplicationException):
    NOISE_MODE_UNDEFINED: TemplateException = TemplateException(
        message='Noise mode undefined',
        long_message='Noise mode undefined'
    )

    _message = EnumExceptionStandardMessage.PARAMETERS_PARSE_CONSOLE_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.PARAMETERS_PARSE_CONSOLE_EXCEPTION.value
