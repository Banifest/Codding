# coding=utf-8
from enum import Enum


class EnumBitTransferResult(Enum):
    SUCCESS = "success"
    REPAIR = "repair"
    ERROR = "error"
    SHADOW = "error"
