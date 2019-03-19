# coding=utf-8
from typing import List

from src.coders.convolutional.coder import Coder as Convolutional
from src.coders.cyclical.coder import Coder as Cyclical
from src.coders.fountain.luby_transform import Coder as LubyTransform
from src.coders.linear.hamming import Coder as Hamming
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.endpoint.general_coder_simulate import GeneralCoderSimulate
from src.statistics.db.enum_coders_type import EnumCodersType


class ConsoleCoderSimulate(GeneralCoderSimulate):
    def __init__(
            self,
            coder_type_int: int,
            coder_parsers: List[AbstractGroupParser],
    ):
        if self._coderTypeInt == EnumCodersType.HAMMING.value:
            coder_parser: Hamming.HammingCoderParser = ConsoleCoderSimulate._parser_searcher(
                coder_class=Hamming.HammingCoderParser,
                coder_parsers=coder_parsers
            )
            super().__init__(
                coder_type_int=coder_type_int,
                hem_size_pack=coder_parser.hamming_package_length,
            )
        elif self._coderTypeInt == EnumCodersType.CYCLICAL.value:
            coder_parser: Cyclical.CyclicalCoderParser = ConsoleCoderSimulate._parser_searcher(
                coder_class=Cyclical.CyclicalCoderParser,
                coder_parsers=coder_parsers
            )
            super().__init__(
                coder_type_int=coder_type_int,
                cyc_size_pack=coder_parser.cyclic_package_length,
                cyc_poly=coder_parser.cyclic_polynomial,
            )
        elif self._coderTypeInt == EnumCodersType.CONVOLUTION.value:
            coder_parser: Convolutional.ConvolutionCoderParser = ConsoleCoderSimulate._parser_searcher(
                coder_class=Convolutional.ConvolutionCoderParser,
                coder_parsers=coder_parsers
            )
            super().__init__(
                coder_type_int=coder_type_int,
                con_count_reg=coder_parser.convolution_memory_register,
                con_list_poly=coder_parser.convolution_polynomial_list,
            )
        elif self._coderTypeInt == EnumCodersType.FOUNTAIN.value:
            coder_parser: LubyTransform.FountainCoderParser = ConsoleCoderSimulate._parser_searcher(
                coder_class=LubyTransform.FountainCoderParser,
                coder_parsers=coder_parsers
            )
            super().__init__(
                coder_type_int=coder_type_int,
                fou_size_pack=coder_parser.fountain_package_length,
                fou_size_block=coder_parser.fountain_block_size,
                fou_count_block=coder_parser.fountain_count_block,
            )

    @staticmethod
    def _parser_searcher(
            coder_class: AbstractGroupParser.__class__,
            coder_parsers: List[AbstractGroupParser],
    ):
        for iterator in coder_parsers:
            if isinstance(iterator, coder_class):
                return iterator

    def create_coder(self):
        super().create_coder()
