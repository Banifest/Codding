# coding=utf-8
import argparse
from typing import Optional

from src.channel.enum_codec_type import EnumCodecType
from src.endpoint.console.abstract_subparser import AbstractSubParser
from src.helper.error.exception.parameters_parse_exception import ParametersParseException
from src.helper.pattern.singleton import Singleton


class CodecParser(AbstractSubParser, metaclass=Singleton):
    """
    Parser class for Codec Configure Attributes
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
            "-cm", "--codec",
            required=False,
            help="""Coder mode(s - codec contain only one coder, c - codec contain cascade from two coders )"""
        )

        self._argument_parser.add_argument(
            "-nt", "--noises_type",
            required=False,
            help="""Type of noises(s - for single noise type(Gauss noise) or p - for packages error)"""
        )

        self._argument_parser.add_argument(
            "-ns", "--noise_start",
            required=False,
            help="""Start of noise(from 1.0 to 50.0)"""
        )

        self._argument_parser.add_argument(
            "-ne", "--noise_end",
            required=False,
            help="""End of noise(from 1.0 to 50.0), but lt Start of noise"""
        )

        # We should parse arguments only for unique coder
        if self._argument_group is None:
            self._arguments = vars(self._argument_parser.parse_args())

    @property
    def codec_type(self) -> EnumCodecType:
        """
        :return: Type of Codec like EnumCodecType
        """
        codec_type: Optional[str] = self._arguments["codec"]

        if codec_type is None or codec_type == EnumCodecType.SINGLE.value:
            return EnumCodecType.SINGLE
        elif codec_type == EnumCodecType.CASCADE.value:
            return EnumCodecType.CASCADE
        else:
            raise ParametersParseException(long_message="""Unknown codec type""")
