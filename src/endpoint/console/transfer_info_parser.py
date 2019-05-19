# coding=utf-8
import argparse
from typing import Optional

from src.endpoint.console.abstract_group_parser import AbstractGroupParser


class TransferInfoParser(AbstractGroupParser):
    """
    Parser class for Codec Configure Attributes
    """
    _test_transfer_info: int
    __TRANSFER_INFO_PARAMETER: str = "test_transfer_info"
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
            "-tti", "--{0}".format(self.__TRANSFER_INFO_PARAMETER),
            type=int,
            required=False,
            help="""Information which will be transferred via chanel"""
        )

        self._argumentParser.add_argument(
            "-tqc", "--{0}".format(self.__TEST_QUANTITY_CYCLES),
            type=int,
            required=False,
            help="""How much test will be do"""
        )

    @property
    def test_transfer_info(self) -> Optional[int]:
        return self._arguments[self.__TRANSFER_INFO_PARAMETER]

    @property
    def test_quantity_cycles(self) -> Optional[int]:
        return self._arguments[self.__TEST_QUANTITY_CYCLES]
