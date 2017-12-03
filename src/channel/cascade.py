from math import ceil
from typing import Optional

from src.channel import channel
from src.coders import abstractCoder
from src.coders.casts import BitListToInt
from src.coders.interleaver import Interleaver


class Cascade(channel.Channel):
    firstCoder: abstractCoder.AbstractCoder
    firstInterleaver: Interleaver.Interleaver
    secondCoder: abstractCoder.AbstractCoder
    secondInterleaver: Interleaver.Interleaver = None

    def __init__(self,
                 firstCoder: abstractCoder.AbstractCoder,
                 secondCoder: abstractCoder.AbstractCoder,
                 noiseProbability: int or float,
                 countCyclical: Optional[int],
                 duplex: Optional[bool],
                 firstInterleaver: Optional[Interleaver.Interleaver],
                 secondInterleaver: Interleaver.Interleaver or None):
        super().__init__(None, noiseProbability, countCyclical, duplex, firstInterleaver)
        self.firstCoder = firstCoder
        self.secondCoder = secondCoder

        self.secondInterleaver = secondInterleaver if secondInterleaver is not None else None

    def transfer_one_step(self, information: list) -> [int, int, int]:
        #  Разбиение на пакеты
        package_list = []
        if self.coder.is_div_into_package:
            for x in range(int(ceil(len(information) / self.firstCoder.lengthInformation))):
                package_list.append(
                    information[self.firstCoder.lengthInformation * x:min(self.firstCoder.lengthInformation * (x + 1),
                                                                          len(information))])

        status: list = []
        for x in package_list:
            self.coder = self.secondCoder
            normalization_information = self.firstCoder.try_normalization(x)

            now_information: list = self.firstCoder.Encoding(normalization_information)

            if self.secondInterleaver is not None:
                now_information = self.secondInterleaver.Shuffle(now_information)

            status: list = self.get_transfer_one_step(now_information)

            # обрезка добавленных битов для нормализации
            now_information = status[0][-len(now_information):]

            if self.secondInterleaver is not None:
                now_information = self.secondInterleaver.Reestablish(now_information)

            now_information = self.firstCoder.Decoding(now_information)

            if BitListToInt(now_information) != BitListToInt(normalization_information):
                return [2, status[1], status[2]]
        return [1, status[1], status[2]]
