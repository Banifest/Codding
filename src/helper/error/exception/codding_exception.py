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

    LENGTH_OF_CURRENT_SOURCE_STATE_DIFF: TemplateException = TemplateException(
        message="Length of current and source states doesn't equal",
        long_message="""
                    Length of current state is {0}.
                    Length of source state is {1}
                    """
    )

    LACKS_OF_BLOCKS_FOR_DECODING: TemplateException = TemplateException(
        message="Lacks of blocks for decoding package with fountain coder",
        long_message="Lacks of blocks for decoding package with fountain coder",
    )
