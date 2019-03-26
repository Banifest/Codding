# coding=utf-8
# coding=utf-8
import argparse
import random
from sqlite3 import Connection
from typing import Optional
from uuid import UUID

from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int, bit_list_to_int_list, int_to_bit_list
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.helper.error.exception.GUI.setting_exception import SettingException
from src.helper.error.exception.codding_exception import CodingException
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType
from src.statistics.db.table import fountain_table


class Coder(abstract_coder.AbstractCoder):
    type_of_coder = EnumCodersType.FOUNTAIN

    _name = "Fountain"
    # quantity information blocks
    _countCodingBlocks: int
    # quantity of combination blocks
    _countBlocks: int
    # size of one block
    _sizeBlock: int
    # combination blocks
    _blocks: list

    def __init__(self, size_block: int, count_coding_blocks: int, length_information: int):
        log.debug("Creation of fountain coder with parameters: {0}, {1}, {2}".
                  format(size_block, count_coding_blocks, length_information))
        self.lengthInformation = length_information
        self._sizeBlock = size_block
        self._blocks = []
        self._countCodingBlocks = count_coding_blocks
        # целочисленное деление с округлением вверх
        self._countBlocks = ((length_information - 1) // self._sizeBlock) + 1
        # генератор случайных чисел
        random_generator: random.Random = random.Random(random.random() * 50)
        # Генерация блоков сочетаний
        set_combination_blocks: set = set()
        while len(set_combination_blocks) < self._countCodingBlocks:
            if 2 ** self._countBlocks - 1 == len(set_combination_blocks):
                raise SettingException(
                    message="Error occurs during creation Fountain coder"
                )
            set_combination_blocks.add(random_generator.getrandbits(self._countBlocks))
            set_combination_blocks -= {0}

        self._blocks: list = list(set_combination_blocks)
        self.lengthInformation = length_information
        self.lengthAdditional = size_block * count_coding_blocks - length_information
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

    def encoding(self, information: list):
        log.info("Fountain LT-coder start coding of package {0}".format(information))
        combination_blocks: list = []
        information = [0] * abs(len(information) - self.lengthInformation) + information  # добавление 0 битов вначало
        for x in range(0, len(information), self._sizeBlock):
            combination_blocks.append(bit_list_to_int(information[x:min(x + self._sizeBlock, len(information))]))

        answer: list = []

        for x in range(self._countCodingBlocks):
            value: int = 0
            count: int = 0
            for y in int_to_bit_list(self._blocks[x], self._countBlocks):
                if y == 1:
                    value ^= combination_blocks[count]
                count += 1
            answer.append(int_to_bit_list(value, self._sizeBlock))

        return [y for x in answer for y in x]

    def decoding(self, information: list):
        """
        Декодер LT-фонтанного кода с заранее установленным генератором случайных чисел
        :param information: list Закодированная информация, представленная в виде массива битов
        :return: list Декодированная информация, представленная в виде массива битов
        """
        log.info("Fountain LT-decoder decoding of package {0}".format(information))
        decoded_set_list: list = [set(bit_list_to_int_list(int_to_bit_list(x, self._sizeBlock))) for x in self._blocks]
        decoded_set_list.append(set())  # костыль, чтобы работало
        is_kill: bool = False

        # Divided into blocks
        status: list = [False for x in range(self._countBlocks)]
        status.append(True)  # One block should be always true

        temp_list: list = []
        for x in range(0, len(information), self._sizeBlock):
            temp: list = []
            for y in range(self._sizeBlock):
                if (x + y) < len(information):
                    temp.append(information[x + y])
            temp_list.append(bit_list_to_int(temp))
        temp_list.append(0)  # One block should be always 0

        answer: list = [0] * self._countCodingBlocks
        while not is_kill and {True} != set(status):
            is_kill = True
            for x in range(len(decoded_set_list)):
                for y in range(len(decoded_set_list)):
                    difference = decoded_set_list[x] - decoded_set_list[y]
                    if len(difference) == 1 and (decoded_set_list[y] - decoded_set_list[x]) == set():
                        is_kill = False
                        status[list(difference)[0]] = True
                        answer[list(difference)[0]] = temp_list[x] ^ temp_list[y]
                        for z in range(len(decoded_set_list)):
                            if list(difference)[0] in decoded_set_list[z]:
                                temp_list[z] ^= answer[list(difference)[0]]
                                decoded_set_list[z] = decoded_set_list[z] - difference

        if set(status) != {True}:
            log.debug("Lacks of blocks for decoding package with fountain coder")
            raise CodingException(
                message=CodingException.LACKS_OF_BLOCKS_FOR_DECODING.message,
                long_message=CodingException.LACKS_OF_BLOCKS_FOR_DECODING.long_message
            )

        # Form result in digital format
        answer = answer[:-1]
        answer = [int_to_bit_list(answer[0])] + [int_to_bit_list(x, self._sizeBlock) for x in answer[1:]]
        answer.reverse()
        return [y for x in answer for y in x]

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    def get_speed(self) -> float:
        return super().get_speed()

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'length information word': self.lengthInformation,
            'length additional bits': self.lengthAdditional,
            'length coding word': self.lengthTotal,
            'speed': self.get_speed()
        }

    def save_to_database(self, coder_guid: UUID, connection: Connection) -> None:
        connection.execute(fountain_table.insert(
            guid=coder_guid,
            count_info_block=self._countCodingBlocks,
            count_block=self._countBlocks,
            block_size=self._sizeBlock,
            block_array=self._blocks,
        ))

    class FountainCoderParser(AbstractGroupParser):
        _prefix: str = ""
        __PACKAGE_LENGTH: str = "fountain_package_length"
        __BLOCK_SIZE: str = "fountain_block_size"
        __QUANTITY_BLOCK: str = "fountain_quantity_block"

        def __init__(
                self,
                argument_parser: Optional[argparse.ArgumentParser] = None,
                argument_group=None,
                prefix: str = ""
        ):
            super().__init__(
                argument_parser=argument_parser,
                argument_group=argument_group
            )
            self._prefix = prefix

            self._argument_parser.add_argument(
                "-{0}fntpl".format(prefix), "--{0}{1}".format(prefix, self.__PACKAGE_LENGTH),
                type=int,
                help="""Length of package for Fountain coder"""
            )

            self._argument_parser.add_argument(
                "-{0}fntbs".format(prefix), "--{0}{1}".format(prefix, self.__BLOCK_SIZE),
                type=int,
                help="""Size of block of Fountain coder"""
            )

            self._argument_parser.add_argument(
                "-{0}fntqb".format(prefix), "--{0}{1}".format(prefix, self.__QUANTITY_BLOCK),
                type=int,
                help="""Quantity of blocks of Fountain coder"""
            )

            # We should parse arguments only for unique coder
            if self._argument_group is None:
                self.arguments = vars(self._argument_parser.parse_args())

        @property
        def fountain_package_length(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__PACKAGE_LENGTH)]

        @property
        def fountain_block_size(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__BLOCK_SIZE)]

        @property
        def fountain_count_block(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__QUANTITY_BLOCK)]

    @staticmethod
    def get_coder_parameters(
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None,
            prefix: str = ""
    ):
        return Coder.FountainCoderParser(
            argument_parser=argument_parser,
            argument_group=argument_group,
            prefix=prefix
        )
