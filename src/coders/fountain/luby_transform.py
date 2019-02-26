# coding=utf-8
# coding=utf-8
import random

from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int, bit_list_to_int_list, int_to_bit_list
from src.helper.error.exception.codding_exception import CodingException
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType


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
                raise CodingException()
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

    def get_coder_parameters(self):
        pass

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
