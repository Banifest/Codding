# coding=utf-8
import argparse
from enum import Enum
from typing import Optional, List

from src.coders.abstract_coder import AbstractCoder
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.endpoint.console.codec_parser import CodecParser
from src.endpoint.console.coder_parser import CoderParser
from src.endpoint.console.enum_app_mode import EnumAppMode
from src.endpoint.console.transfer_info_parser import TransferInfoParser
from src.helper.error.exception.parameters_parse_exception import ParametersParseException
from src.helper.pattern.singleton import Singleton


class AppParser(metaclass=Singleton):
    class EnumCoderSequence(Enum):
        FIRST = "f"
        SECOND = "s"

    __MODE_PARAMETERS: str = "mode"
    _arguments: None
    _argument_parser = argparse.ArgumentParser()
    _codec_parser: CodecParser
    _coder_parser: CoderParser
    _transfer_info_parser: TransferInfoParser
    _first_coder_parsers: List[AbstractGroupParser] = []
    _second_coder_parsers: List[AbstractGroupParser] = []

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None
    ):
        if argument_parser:
            self._argument_parser = argument_parser
        else:
            self._argument_parser = argparse.ArgumentParser(prog="Diploma")

        self._argument_parser.add_argument(
            "-m", "--{0}".format(self.__MODE_PARAMETERS),
            required=False,
            help="""Type of running mode (GUI - {0}, console - {1})""".format(
                EnumAppMode.GUI.value,
                EnumAppMode.CONSOLE.value
            )
        )

        # Add subparsers hire
        self._codec_parser = CodecParser(argument_group=self._argument_parser.add_argument_group("cm", "Codec mode"))
        self._coder_parser = CoderParser(argument_group=self._argument_parser.add_argument_group("ct", "Coder type"))
        self._coders_template_generate()

        self._arguments = vars(self._argument_parser.parse_args())
        self._coder_parser.arguments = self._arguments
        self._codec_parser.arguments = self._arguments
        self._coders_define_arguments()

    @property
    def app_mode(self) -> EnumAppMode:
        app_mode: Optional[str] = self._arguments[AppParser.__MODE_PARAMETERS]

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

    @property
    def coder_parser(self) -> CoderParser:
        return self._coder_parser

    @property
    def codec_parser(self) -> CodecParser:
        return self._codec_parser

    @property
    def first_coders(self) -> List[AbstractGroupParser]:
        return self._first_coder_parsers

    @property
    def second_coders(self) -> List[AbstractGroupParser]:
        return self._second_coder_parsers

    # noinspection SpellCheckingInspection
    def _coders_template_generate(self):
        for iterator in AbstractCoder.get_inheritors_coder_classes():
            self._first_coder_parsers.append(iterator.get_coder_parameters(
                argument_group=self._argument_parser.add_argument_group("frtcdr", "First Coder"),
                prefix=self.EnumCoderSequence.FIRST.value
            ))

            self._second_coder_parsers.append(iterator.get_coder_parameters(
                argument_group=self._argument_parser.add_argument_group("sndcdr", "Second Coder"),
                prefix=self.EnumCoderSequence.SECOND.value
            ))

    def _coders_define_arguments(self):
        for iterator in self._first_coder_parsers + self._second_coder_parsers:
            iterator.arguments = self._arguments
