# coding=utf-8
from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.exception.application_exception import ApplicationException
from src.helper.error.exception.template_exception import TemplateException


class ParametersParseException(ApplicationException):
    NOISE_MODE_UNDEFINED: TemplateException = TemplateException(
        message='Noise mode undefined',
        long_message='Noise mode undefined'
    )

    INFORMATION_NOT_SERIALIZABLE: TemplateException = TemplateException(
        message='Information cannot be serialize',
        long_message='Specify integer in test information field'
    )

    APPLICATION_MODE_UNDEFINED: TemplateException = TemplateException(
        message="Unknown application running mode",
        long_message="Application cannot start with provided application running mode equals {0}"
    )

    START_NOISE_LE_END: TemplateException = TemplateException(
        message="Start noise should be less them end noise",
        long_message="Start noise should be less them end noise"
    )

    INTERLEAVER_SETTING: TemplateException = TemplateException(
        message="Incorrect interleaver settings",
        long_message="Change interleaver setting",
    )

    _message = EnumExceptionStandardMessage.PARAMETERS_PARSE_CONSOLE_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.PARAMETERS_PARSE_CONSOLE_EXCEPTION.value
