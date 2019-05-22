from enum import Enum


class EnumCoderTableName(Enum):
    HAMMING = "hamming"
    CYCLIC = "cyclic"
    FOUNTAIN = "fountain"
    CONVOLUTION = "convolution"
    TEST_RESULT = "test_result"
    CODER = "_coder"
    CASE_RESULT = "case_result"
