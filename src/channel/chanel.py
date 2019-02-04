# coding=utf-8
import random
from math import ceil
from typing import Union, Optional, List

from src.channel.ChanelException import ChanelException
from src.helper.pattern.singleton import Singleton
from src.logger import log


class Chanel(metaclass=Singleton):
    """
    Chanel
    """
    __straight: float = 10.0
    __package_len: int

    def __init__(
            self,
            straight: Optional[Union[float, int]] = None,
    ):
        if straight is not None:
            self.__straight = straight

    # noinspection PyMethodMayBeStatic
    def divide_on_blocks(self, information: list, block_len: int) -> List[list]:
        """

        :param information:
        :param block_len:
        :return:
        """
        if len(information) >= block_len:
            return [information]

        blocks: list = []
        for number_of_block in range(ceil(block_len / len(information))):
            blocks.append(information[number_of_block * block_len: (number_of_block + 1) * block_len])

        return blocks

    def gen_interference(self, information: list, straight: float = None) -> list:
        """
        Генерация помех с задданной вероятностью
        :param information: list Информация, представленная в виде массива битов
        :param straight: Optional[float] Вероятность помех принимает значения от 0.00 до 100.00, может быть опушенна,
        в таком случае будет использоваться значение шума заданное в канале
        :return: Искажённую информацию, представленную в виде массива битов
        """
        if straight is None:
            straight = self.__straight

        log.debug("Симуляция шума на канале с вероятностью {0}".format(straight))

        random_generator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел

        count_change_bit: int = int(len(information) * straight / 100)  # кол-во ошибок на канале
        if count_change_bit == 0 and straight != 0:
            # если ошибок не ноль, то увеличиваем до 1
            count_change_bit = 0

        # множество битов которые будут измененны
        changes_bits: set = set()

        # собираем множество неповторяющихся битов
        while len(changes_bits) < count_change_bit:
            changes_bits.add(random_generator.randint(0, len(information) - 1))

        # преобразуем в список
        changes_bits: list = list(changes_bits)
        answer: list = information.copy()
        # инвертирование битов
        for bit_value in changes_bits:
            answer[bit_value] ^= 1

        log.debug("В ходе симуляции шума пакет преобразовался в {0}".format(answer))
        return answer

    def gen_package_interference(self, information: list, length_of_block: int, straight: float = None,
                                 flg_split_package: bool = False) -> list:
        """
        Генерация помех с задданной вероятностью
        :param flg_split_package: Нужен ли хотябы один правильный символ между пакетами ошибок пакете
        :param information: list Информация, представленная в виде массива битов
        :param length_of_block:
        :param straight: Optional[float] Вероятность помех принимает значения от 0.00 до 100.00, может быть опушенна,
        в таком случае будет использоваться значение шума заданное в канале
        :return: Искажённую информацию, представленную в виде массива битов
        """

        if straight is None:
            straight = self.__straight

        log.debug("Симуляция шума в виде пакета длинной {1} на канале с вероятностью {0}".
                  format(straight, length_of_block))
        begin_package_straight: float = straight / length_of_block
        # count error package of chanel
        count_error_package: int = int(len(information) / begin_package_straight)

        if flg_split_package:
            if count_error_package * length_of_block + count_error_package - 1 >= len(information):
                raise ChanelException(
                    message=ChanelException.PACKET_LENGTH_EXCEEDED,
                    long_message=ChanelException.PACKET_LENGTH_EXCEEDED
                )
        else:
            if count_error_package * length_of_block >= len(information):
                raise ChanelException(
                    message=ChanelException.PACKET_LENGTH_EXCEEDED,
                    long_message=ChanelException.PACKET_LENGTH_EXCEEDED
                )

        # random generator
        random_generator: random.Random = random.Random(random.random() * 50)
        count_free_bits: int = len(information) - count_error_package * length_of_block
        # mask of changed bits
        changes_bits: list = []
        for iterator in range(count_error_package):
            if flg_split_package:
                # we should save bits for split package: count_free_bits - count of package - current step - 1
                count_save_bits: int = count_error_package - iterator - 1
                count_pass_bits = random_generator.randint(1, count_free_bits - count_save_bits)
                changes_bits += count_pass_bits * [0]
                changes_bits += length_of_block * [1]
            else:
                count_pass_bits = random_generator.randint(0, count_free_bits)
                if count_pass_bits != 0:
                    changes_bits += count_pass_bits * [0]
                changes_bits += length_of_block * [1]

        result: list = information.copy()
        # inversion of bits
        for bit_value in changes_bits:
            result[bit_value] ^= 1

        log.debug("В ходе симуляции шума пакет преобразовался в {0}".format(result))
        return result
