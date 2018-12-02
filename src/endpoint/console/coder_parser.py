# coding=utf-8
import argparse
from typing import Optional

from src.helper.pattern.singleton import Singleton
from src.statistics.db.enum_coders_type import EnumCodersType


class CoderParser(metaclass=Singleton):
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
            self._argument_parser = self._subparsers.add_parser("-ct")
        else:
            self._subparsers = self._argument_parser

        self._argument_parser.add_argument(
            "-ct", "--coder_type",
            required=False,
            help="""Coder type ({0} - convolution, {1} - fountain, {2} - cyclical, {3} - hamming)""".format(
                EnumCodersType.CONVOLUTION.value,
                EnumCodersType.FOUNTAIN.value,
                EnumCodersType.CYCLICAL.value,
                EnumCodersType.HAMMING.value
            )
        )

        self._arguments = vars(self._argument_parser.parse_args())

    def get_argument_parser(self) -> argparse.ArgumentParser:
        return self._argument_parser
