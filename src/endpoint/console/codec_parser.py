# coding=utf-8
import argparse
from typing import Optional

from src.channel.enum_codec_type import EnumCodecType
from src.helper.error.exception.parameters_parse_exception import ParametersParseException
from src.helper.pattern.singleton import Singleton


class CodecParser(metaclass=Singleton):
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
            self._argument_parser = argparse.ArgumentParser().add_subparsers()

        if subparsers is not None:
            self._subparsers = subparsers
            self._argument_parser = self._subparsers.add_parser("cm", aliases=["coder_mode"], help="-cm help")
        else:
            self._subparsers = self._argument_parser

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
        if self._subparsers is None:
            self._arguments = vars(self._argument_parser.parse_args())

    @property
    def get_codec_type(self) -> EnumCodecType:
        """
        TODO add documentation
        :return:
        """
        codec_type: Optional[str] = self._arguments["codec"]

        if codec_type is None or codec_type == EnumCodecType.SINGLE.value:
            return EnumCodecType.SINGLE
        elif codec_type == EnumCodecType.CASCADE.value:
            return EnumCodecType.CASCADE
        else:
            raise ParametersParseException(long_message="""Unknown codec type""")

    def get_argument_parser(self) -> argparse.ArgumentParser:
        """
        TODO
        :return:
        """
        return self._argument_parser
