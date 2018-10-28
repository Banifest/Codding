from src.helper.error.EnumExceptionStandardMessage import EnumExceptionStandardMessage
from src.helper.error.EnumMessageType import EnumMessageType


class ApplicationException(Exception):
    _message: str = EnumExceptionStandardMessage.APPLICATION_EXCEPTION.value
    _long_message: str = EnumExceptionStandardMessage.APPLICATION_EXCEPTION.value
    _message_type: EnumMessageType = EnumMessageType.ERROR

    def __init__(self, message: str = "", long_message: str = "",
                 message_type: EnumMessageType = EnumMessageType.ERROR):
        self._message = message
        if long_message == "":
            self._long_message = message
        else:
            self._long_message = long_message
        self._message_type = message_type

    def get_message(self) -> str:
        return self._message

    def get_long_message(self) -> str:
        return self._long_message
