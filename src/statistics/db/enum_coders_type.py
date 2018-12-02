# coding=utf-8
from enum import Enum, auto


class EnumCodersType(Enum):
    HAMMING = auto()
    CYCLICAL = auto()
    CONVOLUTION = auto()
    FOUNTAIN = auto()
