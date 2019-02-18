# coding=utf-8

from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage

from src.helper.error.exception.application_exception import ApplicationException
from src.helper.error.exception.template_exception import TemplateException


class CodingException(ApplicationException):
    _message = EnumExceptionStandardMessage.CODER_EXCEPTION.value
    _long_message = EnumExceptionStandardMessage.CODER_EXCEPTION.value

    LENGTH_OF_INPUT_PACKAGE_OVERFLOW: TemplateException = TemplateException(
        message="Length of input package overflow for coder {0}",
        long_message="""
                Length of input package overflow for coder {0}.
                Max possible length of package equals {1}, but current length is {2}
                """
    )
