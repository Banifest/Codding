# coding=utf-8
import argparse
from typing import Optional

from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.statistics.db.enum_coders_type import EnumCodersType


class CoderParser(AbstractGroupParser):
    """
    Parser class for Coder Type Attributes
    """

    __CODER_TYPE: str = "coder_type"

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None
    ):
        super().__init__(
            argument_parser=argument_parser,
            argument_group=argument_group
        )

        self._argument_parser.add_argument(
            "-ct", "--{0}".format(self.__CODER_TYPE),
            # choices=(
            #     EnumCodersType.CONVOLUTION.value,
            #     EnumCodersType.FOUNTAIN.value,
            #     EnumCodersType.CYCLICAL.value,
            #     EnumCodersType.HAMMING.value
            # ),
            help="""Coder type (convolution - {0}, fountain - {1}, cyclical - {2}, hamming - {3})""".format(
                EnumCodersType.CONVOLUTION.value,
                EnumCodersType.FOUNTAIN.value,
                EnumCodersType.CYCLICAL.value,
                EnumCodersType.HAMMING.value
            )
        )

        # We should parse arguments only for unique coder
        if self._argument_group is None:
            self.arguments = vars(self._argument_parser.parse_args())

    @property
    def coder_type(self) -> int:
        return int(self._arguments[self.__CODER_TYPE])
