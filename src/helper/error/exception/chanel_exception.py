# coding=utf-8
from src.helper.error.exception.application_exception import ApplicationException
from src.helper.error.exception.template_exception import TemplateException


class ChanelException(ApplicationException):
    PACKET_LENGTH_EXCEEDED: TemplateException = TemplateException(
        message="Error packet length exceeded for package errors generate",
        long_message="Error packet length exceeded for package errors generate"
    )
