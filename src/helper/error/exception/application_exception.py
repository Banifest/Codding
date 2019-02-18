# coding=utf-8
from typing import Optional

from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.enum_message_type import EnumMessageType


class ApplicationException(Exception):
    _message: str = EnumExceptionStandardMessage.APPLICATION_EXCEPTION.value
    _long_message: str = EnumExceptionStandardMessage.APPLICATION_EXCEPTION.value
    _message_type: EnumMessageType = EnumMessageType.ERROR

    def __init__(
            self,
            message: Optional[str] = None,
            long_message: Optional[str] = None,
            message_type: EnumMessageType = EnumMessageType.ERROR
    ):
        if message is not None:
            self._message = message

        if long_message is None and message is not None:
            self._long_message = message
        elif long_message is not None:
            self._long_message = long_message

        self._message_type = message_type

    def __str__(self) -> str:
        return """Exception was occur with type {0}. {1}. {2}""".format(
            self._message_type,
            self._message,
            self._long_message
        )

    def get_message(self) -> str:
        return self._message

    def get_long_message(self) -> str:
        return self._long_message
