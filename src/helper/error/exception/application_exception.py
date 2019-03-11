# coding=utf-8
from typing import Optional, List, Any

from src.helper.error.enum_exception_standard_message import EnumExceptionStandardMessage
from src.helper.error.enum_message_type import EnumMessageType


class ApplicationException(Exception):
    _message: str = EnumExceptionStandardMessage.APPLICATION_EXCEPTION.value
    _long_message: str = EnumExceptionStandardMessage.APPLICATION_EXCEPTION.value
    _message_type: EnumMessageType = EnumMessageType.ERROR
    _previous: Exception

    def __init__(
            self,
            message: Optional[str] = None,
            long_message: Optional[str] = None,
            message_type: EnumMessageType = EnumMessageType.ERROR,
            additional_information: List[Any] = None,
            previous: Optional[Exception] = None
    ):

        if message is not None:
            self._message = message if additional_information is None \
                else message.format(*additional_information)

        if long_message is None and message is not None:
            self._long_message = message if additional_information is None else message.format(
                *additional_information)

        elif long_message is not None:
            self._long_message = long_message if additional_information is None else long_message.format(
                *additional_information)

        self._message_type = message_type
        self._previous = previous

    @property
    def previous(self):
        return self._previous

    def __str__(self) -> str:
        return """Exception was occurs with type {0}. {1}. {2}""".format(
            self._message_type,
            self._message,
            self._long_message
        )

    def get_message(self) -> str:
        return self._message

    def get_long_message(self) -> str:
        return self._long_message
