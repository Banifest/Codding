# coding=utf-8
import argparse
from typing import Optional

from src.channel.enum_codec_type import EnumCodecType
from src.endpoint.console.enum_app_mode import EnumAppMode
from src.helper.error.exception.GUI.parameters_parse_exception import ParametersParseException
from src.helper.pattern.singleton import Singleton


class Parser(metaclass=Singleton):
    _argument_parser = argparse.ArgumentParser()
    _arguments: None

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None
    ):
        if argument_parser:
            self._argument_parser = argument_parser
        else:
            self._argument_parser = argparse.ArgumentParser()

        self._argument_parser.add_argument(
            "-m", "--mode",
            required=False,
            help="""Type of running mode (g - for gui, c - console)"""
        )
        self._argument_parser.add_argument(
            "-cm", "--codec",
            required=False,
            help="""Coder mode(s - codec contain only one coder, c - codec contain cascade from two coders )"""
        )
        self._argument_parser.add_argument_group(
            "-nt", "--noises_type",
            required=False,
            help="""Type of noises(s - for single noise type(Gauss noise) or p - for packages error)"""
        )

        self._arguments = vars(self._argument_parser.parse_args())

    @property
    def get_app_mode(self) -> EnumAppMode:
        app_mode: Optional[str] = self._arguments["mode"]

        if app_mode is None or app_mode == EnumAppMode.GUI.value:
            return EnumAppMode.GUI
        elif app_mode == EnumAppMode.CONSOLE.value:
            return EnumAppMode.CONSOLE
        else:
            raise ParametersParseException(long_message="""Unknown application running mode""")

    @property
    def get_codec_type(self) -> EnumCodecType:
        codec_type: Optional[str] = self._arguments["codec"]

        if codec_type is None or codec_type == EnumCodecType.SINGLE.value:
            return EnumCodecType.SINGLE
        elif codec_type == EnumCodecType.CASCADE.value:
            return EnumCodecType.CASCADE
        else:
            raise ParametersParseException(long_message="""Unknown codec type""")
