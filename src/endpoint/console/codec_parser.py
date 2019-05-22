# coding=utf-8
import argparse
from typing import Optional

from src.channel.enum_codec_type import EnumCodecType
from src.channel.enum_noise_mode import EnumNoiseMode
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.helper.error.exception.parameters_parse_exception import ParametersParseException


class CodecParser(AbstractGroupParser):
    """
    Parser class for Codec Configure Attributes
    """
    __CODEC_OPTION: str = "codec"
    __NOISE_TYPE_OPTION: str = "noises_type"
    __NOISE_START_OPTION: str = "noise_start"
    __NOISE_END_OPTION: str = "noise_end"
    __INFORMATION_FOR_TEST: str = "information_for_test"
    __NOISE_PACKAGE_LENGTH: str = "noise_package_length"
    __NOISE_PACKAGE_PERIOD: str = "noise_package_period"
    __TEST_QUANTITY_CYCLES: str = "test_quantity_cycles"

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
            "-cm", "--{0}".format(__class__.__CODEC_OPTION),
            required=False,
            type=str,
            choices=(EnumCodecType.SINGLE.value, EnumCodecType.CASCADE.value,),
            help="""Coder mode({0} - codec contain only one _coder, 
            {1} - codec contain cascade from two coders )""".format(
                EnumCodecType.SINGLE.value,
                EnumCodecType.CASCADE.value,
            )
        )

        self._argumentParser.add_argument(
            "-nt", "--{0}".format(__class__.__NOISE_TYPE_OPTION),
            required=False,
            type=str,
            choices=(EnumNoiseMode.SINGLE.value, EnumNoiseMode.PACKAGE.value, EnumNoiseMode.MIX.value,),
            help="""Type of noises({0} - for single noise type(Gauss noise) or {1} - for packages error, 
            {2} - for mix error)""".format(
                EnumNoiseMode.SINGLE.value,
                EnumNoiseMode.PACKAGE.value,
                EnumNoiseMode.MIX.value,
            )
        )

        self._argumentParser.add_argument(
            "-ns", "--{0}".format(__class__.__NOISE_START_OPTION),
            required=False,
            type=float,
            help="""Start of noise(from 1.0 to 50.0)"""
        )

        self._argumentParser.add_argument(
            "-ne", "--{0}".format(__class__.__NOISE_END_OPTION),
            required=False,
            type=float,
            help="""End of noise(from 1.0 to 50.0), but lt Start of noise"""
        )

        self._argumentParser.add_argument(
            "-ift", "--{0}".format(self.__INFORMATION_FOR_TEST),
            required=False,
            type=int,
            help="""Information for testing process"""
        )

        self._argumentParser.add_argument(
            "-npl", "--{0}".format(self.__NOISE_PACKAGE_LENGTH),
            required=False,
            type=int,
            help="""Length of package"""
        )

        self._argumentParser.add_argument(
            "-npp", "--{0}".format(self.__NOISE_PACKAGE_PERIOD),
            required=False,
            type=int,
            help="""Period of package"""
        )

        self._argumentParser.add_argument(
            "-tqc", "--{0}".format(self.__TEST_QUANTITY_CYCLES),
            type=int,
            required=False,
            help="""How much test will be do"""
        )

        # We should parse arguments only for unique _coder
        if self._argumentGroup is None:
            self._arguments = vars(self._argumentParser.parse_args())

    @property
    def codec_type(self) -> EnumCodecType:
        """
        :return: Type of Codec like EnumCodecType
        """
        codec_type: Optional[str] = self._arguments[self.__CODEC_OPTION]

        if codec_type is None or codec_type == EnumCodecType.SINGLE.value:
            return EnumCodecType.SINGLE
        elif codec_type == EnumCodecType.CASCADE.value:
            return EnumCodecType.CASCADE
        else:
            raise ParametersParseException(long_message="""Unknown codec type""")

    @property
    def noise_type(self) -> EnumNoiseMode:
        """
        :return: Type of Codec like EnumCodecType
        """
        if self._arguments[self.__NOISE_TYPE_OPTION] is not None:
            noise_type: Optional[str] = self._arguments[self.__NOISE_TYPE_OPTION]
        else:
            noise_type = None

        if noise_type is None or noise_type == EnumNoiseMode.SINGLE.value:
            return EnumNoiseMode.SINGLE
        elif noise_type == EnumNoiseMode.PACKAGE.value:
            return EnumNoiseMode.CASCADE
        elif noise_type == EnumNoiseMode.MIX.value:
            return EnumNoiseMode.MIX
        else:
            raise ParametersParseException(long_message="""Unknown codec type""")

    @property
    def noise_start(self) -> float:
        return self._arguments[self.__NOISE_START_OPTION]

    @property
    def noise_end(self) -> float:
        return self._arguments[self.__NOISE_END_OPTION]

    @property
    def info_for_test(self) -> int:
        return self._arguments[self.__INFORMATION_FOR_TEST]

    @property
    def noise_package_length(self) -> int:
        return self._arguments[self.__NOISE_PACKAGE_LENGTH]

    @property
    def noise_package_period(self) -> int:
        return self._arguments[self.__NOISE_PACKAGE_PERIOD]

    @property
    def test_quantity_cycles(self) -> int:
        return self._arguments[self.__TEST_QUANTITY_CYCLES]
