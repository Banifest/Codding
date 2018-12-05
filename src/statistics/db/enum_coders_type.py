# coding=utf-8
from enum import Enum


class EnumCodersType(Enum):
    ABSTRACT = -1
    HAMMING = 0
    CYCLICAL = 1
    CONVOLUTION = 2
    FOUNTAIN = 3
