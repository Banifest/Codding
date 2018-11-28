# coding=utf-8
from enum import Enum, auto, unique


@unique
class EnumMessageType(Enum):
    FAILED = auto()
    ERROR = auto()
    WARNING = auto()
    INFORMATION = auto()
    SUCCESSFUL = auto()
