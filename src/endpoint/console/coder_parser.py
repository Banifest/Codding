# coding=utf-8
import argparse
from typing import Optional

from src.endpoint.console.abstract_subparser import AbstractSubParser
from src.helper.pattern.singleton import Singleton
from src.statistics.db.enum_coders_type import EnumCodersType


class CoderParser(AbstractSubParser, metaclass=Singleton):
    """
    Parser class for Coder Type Attributes
    """

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
            "-ct",
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
