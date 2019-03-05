# coding=utf-8
import argparse
from typing import Optional

from src.endpoint.console.codec_parser import CodecParser
from src.endpoint.console.coder_parser import CoderParser
from src.endpoint.console.enum_app_mode import EnumAppMode
from src.helper.error.exception.parameters_parse_exception import ParametersParseException
from src.helper.pattern.singleton import Singleton


class AppParser(metaclass=Singleton):
    _argument_parser = argparse.ArgumentParser()
    _arguments: None
    _subparsers: None

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

        self._subparsers = self._argument_parser.add_subparsers()

        # Add subparsers hire
        CodecParser(subparsers=self._subparsers)
        CoderParser(subparsers=self._subparsers)

        self._arguments = vars(self._argument_parser.parse_args())

    @property
    def get_app_mode(self) -> EnumAppMode:
        app_mode: Optional[str] = self._arguments["mode"]

        if app_mode is None or app_mode == EnumAppMode.GUI.value:
            return EnumAppMode.GUI
        elif app_mode == EnumAppMode.CONSOLE.value:
            return EnumAppMode.CONSOLE
        else:
            raise ParametersParseException(
                message=ParametersParseException.APPLICATION_MODE_UNDEFINED.message,
                long_message=ParametersParseException.APPLICATION_MODE_UNDEFINED.long_message,
                additional_information=[app_mode]
            )
