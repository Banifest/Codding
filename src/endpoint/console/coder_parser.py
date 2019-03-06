# coding=utf-8
import argparse
from typing import Optional

from src.helper.pattern.singleton import Singleton
from src.statistics.db.enum_coders_type import EnumCodersType


class CoderParser(metaclass=Singleton):
    """
    TODO add documentation
    """
    _argument_parser = argparse.ArgumentParser()
    _arguments: None
    _subparsers: None

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None,
            subparsers: Optional[argparse.ArgumentParser] = None
    ):
        if argument_parser:
            self._argument_parser = argument_parser
        else:
            self._argument_parser = argparse.ArgumentParser()

        if subparsers is not None:
            self._subparsers = subparsers
            self._argument_parser = self._subparsers.add_parser("ct", aliases=["coder_type"], help="help")
        else:
            self._subparsers = self._argument_parser

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
        if self._subparsers is None:
            self._arguments = vars(self._argument_parser.parse_args())

    @property
    def get_argument_parser(self) -> argparse.ArgumentParser:
        """
        TODO
        :return:
        """
        return self._argument_parser
