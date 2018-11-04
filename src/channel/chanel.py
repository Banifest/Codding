import random
from typing import Union, Optional

from src.logger import log


class Chanel:
    __straight: float = 10.0

    def __init__(self, straight: Optional[Union[float, int]] = None):
        self.__straight = straight

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
