# coding=utf-8
from enum import Enum, auto


class EnumCodersType(Enum):
    hamming = auto()
    CYCLICAL = auto()
    CONVOLUTION = auto()
    FOUNTAIN = auto()
