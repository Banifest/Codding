# coding=utf-8
# coding=utf-8
import random

from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int, bit_list_to_int_list, int_to_bit_list
from src.helper.error.exception.CoddingException import CoddingException
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType


class Coder(abstract_coder.AbstractCoder):
    def get_coder_parameters(self):
        pass

    _name = "Фонтанный"
    type_of_coder = EnumCodersType.FOUNTAIN

    _countCodingBlocks: int  # количество блоков информации
    _countBlocks: int  # количество блоков сочетаний
    _sizeBlock: int  # Размер одного блока
    _blocks: list  # блоки сочетаний

    def __init__(self, size_block: int, count_coding_blocks: int, length_information: int):
        log.debug("Создание фонтанного кодера с параметрами:{0}, {1}, {2}".
                  format(size_block, count_coding_blocks, length_information))
        self.lengthInformation = length_information
        self._sizeBlock = size_block
        self._blocks = []
        self._countCodingBlocks = count_coding_blocks
        self._countBlocks = ((
                                     length_information - 1) // self._sizeBlock) + 1  # целочисленное деление с округлением вверх

        random_generator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел
        # Генерация блоков сочетаний
        set_combination_blocks: set = set()
        while len(set_combination_blocks) < self._countCodingBlocks:
            if 2 ** self._countBlocks - 1 == len(set_combination_blocks):
                raise CoddingException()
            set_combination_blocks.add(random_generator.getrandbits(self._countBlocks))
            set_combination_blocks -= {0}

        self._blocks: list = list(set_combination_blocks)
        self.lengthInformation = length_information
        self.lengthAdditional = size_block * count_coding_blocks - length_information
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

    def encoding(self, information: list):
        log.info("Кодирование пакета {0} фонтанным LT-кодером".format(information))
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
        log.info("Декодирование пакета {0} фонтанным LT-декодером".format(information))
        decoded_set_list: list = [set(bit_list_to_int_list(int_to_bit_list(x, self._sizeBlock))) for x in self._blocks]
        decoded_set_list.append(set())  # костыль, чтобы работало
        is_kill: bool = False

        # Разбивка на блоки
        status: list = [False for x in range(self._countBlocks)]
        status.append(True)  # костыль, чтобы работало

        tempList: list = []
        for x in range(0, len(information), self._sizeBlock):
            temp: list = []
            for y in range(self._sizeBlock):
                if (x + y) < len(information):
                    temp.append(information[x + y])
            tempList.append(bit_list_to_int(temp))
        tempList.append(0)  # костыль, чтобы работало

        answer: list = [0] * self._countCodingBlocks
        while not is_kill and {True} != set(status):
            is_kill = True
            for x in range(len(decoded_set_list)):
                for y in range(len(decoded_set_list)):
                    difference = decoded_set_list[x] - decoded_set_list[y]
                    if len(difference) == 1 and (decoded_set_list[y] - decoded_set_list[x]) == set():
                        is_kill = False
                        status[list(difference)[0]] = True
                        answer[list(difference)[0]] = tempList[x] ^ tempList[y]
                        for z in range(len(decoded_set_list)):
                            if list(difference)[0] in decoded_set_list[z]:
                                tempList[z] ^= answer[list(difference)[0]]
                                decoded_set_list[z] = decoded_set_list[z] - difference

        if set(status) != {True}:
            log.debug("Недостаточно блоков для декодирования информации")
            raise CoddingException()

        # формирование ответа в битовом представлении
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
