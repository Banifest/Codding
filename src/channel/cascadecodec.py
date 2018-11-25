# coding=utf-8
# coding=utf-8
from math import ceil
from typing import Optional

from src.channel import codec, chanel
from src.coders import abstract_coder
from src.coders.casts import BitListToInt
from src.coders.interleaver import Interleaver


class CascadeCodec(codec.Codec):
    firstCoder: abstract_coder.AbstractCoder
    firstInterleaver: Interleaver.Interleaver
    secondCoder: abstract_coder.AbstractCoder
    secondInterleaver: Interleaver.Interleaver = None
    mode: int = 0

    def __init__(
            self,
            first_coder: abstract_coder.AbstractCoder,
            second_coder: abstract_coder.AbstractCoder,
            noise_probability: int or float,
            count_cyclical: Optional[int],
            duplex: Optional[bool],
            first_interleaver: Optional[Interleaver.Interleaver],
            second_interleaver: Interleaver.Interleaver or None,
            mode: int = 0
    ):
        super().__init__(None, noise_probability, count_cyclical, duplex, first_interleaver)
        self.firstCoder = first_coder
        self.secondCoder = second_coder
        self.mode = mode

        self.firstInterleaver = first_interleaver if first_interleaver is not None else None
        self.secondInterleaver = second_interleaver if second_interleaver is not None else None

    def transfer_one_step(self, information: list) -> [int, int, int]:
        if self.mode == 0:
            #  Разделение на пакеты
            package_list = []
            if self.firstCoder.is_div_into_package:
                for x in range(int(ceil(len(information) / self.firstCoder.lengthInformation))):
                    package_list.append(
                        information[
                        self.firstCoder.lengthInformation * x: min(
                            self.firstCoder.lengthInformation * (x + 1), len(information)
                        )
                        ])

            status: list = []
            for x in package_list:
                self.coder = self.secondCoder
                normalization_information = self.firstCoder.try_normalization(x)

                now_information: list = self.firstCoder.encoding(normalization_information)

                if self.secondInterleaver is not None:
                    now_information = self.secondInterleaver.shuffle(now_information)

                status: list = self.get_transfer_one_step(now_information)

                # обрезка добавленных битов для нормализации
                now_information = status[0][-len(now_information):]

                if self.secondInterleaver is not None:
                    now_information = self.secondInterleaver.reestablish(now_information)

                now_information = self.firstCoder.decoding(now_information)

                if BitListToInt(now_information) != BitListToInt(normalization_information):
                    return [2, status[1], status[2]]
            return [1, status[1], status[2]]
        elif self.mode == 1:
            first_coder_information: list = self.firstCoder.encoding(information)
            if self.firstInterleaver is not None:
                first_coder_information = self.firstInterleaver.shuffle(first_coder_information)

            second_coder_information: list = self.firstCoder.encoding(information)
            if self.secondInterleaver is not None:
                second_coder_information = self.secondInterleaver.shuffle(second_coder_information)

            status: list = chanel.Chanel().gen_interference(first_coder_information + second_coder_information)

            if self.firstInterleaver is not None:
                first_coder_information = self.firstInterleaver.reestablish(first_coder_information)

            if self.secondInterleaver is not None:
                second_coder_information = self.secondInterleaver.reestablish(second_coder_information)

            first_coder_information = self.firstCoder.decoding(first_coder_information)
            second_coder_information = self.secondCoder.decoding(second_coder_information)
            if BitListToInt(first_coder_information) != BitListToInt(first_coder_information) \
                    and BitListToInt(second_coder_information) != BitListToInt(second_coder_information):
                return [2, status[1], status[2]]
            else:
                return [1, status[1], status[2]]
