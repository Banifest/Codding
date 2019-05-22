# coding=utf-8
import argparse
from typing import Optional

from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.statistics.db.enum_coders_type import EnumCodersType


class CoderParser(AbstractGroupParser):
    """
    Parser class for Coder Type Attributes
    """

    __FIRST_CODER_TYPE: str = "first_coder_type"
    __SECOND_CODER_TYPE: str = "second_coder_type"
    __FIRST_INTERLEAVER_LEN: str = "first_interleaver_length"
    __SECOND_INTERLEAVER_LEN: str = "second_interleaver_length"

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None
    ):
        super().__init__(
            argument_parser=argument_parser,
            argument_group=argument_group
        )

        self._argumentParser.add_argument(
            "-fct", "--{0}".format(self.__FIRST_CODER_TYPE),
            type=int,
            choices=(
                EnumCodersType.CONVOLUTION.value,
                EnumCodersType.FOUNTAIN.value,
                EnumCodersType.CYCLICAL.value,
                EnumCodersType.HAMMING.value
            ),
            help="""Coder type (convolution - {0}, fountain - {1}, cyclical - {2}, hamming - {3})""".format(
                EnumCodersType.CONVOLUTION.value,
                EnumCodersType.FOUNTAIN.value,
                EnumCodersType.CYCLICAL.value,
                EnumCodersType.HAMMING.value
            )
        )

        self._argumentParser.add_argument(
            "-sct", "--{0}".format(self.__SECOND_CODER_TYPE),
            type=int,
            choices=(
                EnumCodersType.CONVOLUTION.value,
                EnumCodersType.FOUNTAIN.value,
                EnumCodersType.CYCLICAL.value,
                EnumCodersType.HAMMING.value
            ),
            help="""Coder type (convolution - {0}, fountain - {1}, cyclical - {2}, hamming - {3})""".format(
                EnumCodersType.CONVOLUTION.value,
                EnumCodersType.FOUNTAIN.value,
                EnumCodersType.CYCLICAL.value,
                EnumCodersType.HAMMING.value
            )
        )

        self._argumentParser.add_argument(
            "-firl", "--{0}".format(self.__FIRST_INTERLEAVER_LEN),
            type=int,
            help="""First length of _interleaver interval"""
        )
        self._argumentParser.add_argument(
            "-sirl", "--{0}".format(self.__SECOND_INTERLEAVER_LEN),
            type=int,
            help="""First length of _interleaver interval"""
        )

        # We should parse arguments only for unique _coder
        if self._argumentGroup is None:
            self.arguments = vars(self._argumentParser.parse_args())

    @property
    def first_interleaver_length(self) -> Optional[int]:
        if self._arguments[self.__FIRST_INTERLEAVER_LEN] is not None:
            return int(self._arguments[self.__FIRST_INTERLEAVER_LEN])
        else:
            return None

    @property
    def second_interleaver_length(self) -> Optional[int]:
        if self._arguments[self.__SECOND_INTERLEAVER_LEN] is not None:
            return int(self._arguments[self.__SECOND_INTERLEAVER_LEN])
        else:
            return None

    @property
    def first_coder_type(self) -> int:
        return int(self._arguments[self.__FIRST_CODER_TYPE])

    @property
    def second_coder_type(self) -> Optional[int]:
        if self._arguments[self.__SECOND_CODER_TYPE] is not None:
            return int(self._arguments[self.__SECOND_CODER_TYPE])
        else:
            return None
