from src.helper.error.exception.application_exception import ApplicationException


class ChanelException(ApplicationException):
    PACKET_LENGTH_EXCEEDED: str = 'Error packet length exceeded'
