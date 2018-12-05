# coding=utf-8
from enum import Enum


class EnumPackageTransferResult(Enum):
    SUCCESS = "success"
    REPAIR = "repair"
    ERROR = "error"
    SHADOW = "error"
