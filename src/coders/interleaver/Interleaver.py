# coding=utf-8
from typing import List

import math

from src.helper.error.exception.parameters_parse_exception import ParametersParseException
from src.logger import log


class Interleaver:
    lengthSmashing: int

    def __init__(self, length_smashing: int):
        self.lengthSmashing = length_smashing

    def shuffle(self, information: List[int]) -> List[int]:
        log.debug("Used interleaver for package {0}".format(information))
        answer: List[int] = []
        try:
            for x in range(self.lengthSmashing):
                is_end: bool = False
                counter: int = 0
                while not is_end:
                    if (counter * self.lengthSmashing + x) < len(information):
                        answer.append(information[counter * self.lengthSmashing + x])
                    else:
                        is_end = True
                    counter += 1
        except IndexError:
            if len(information) % self.lengthSmashing != 0:
                raise ParametersParseException(
                    message=ParametersParseException.INTERLEAVER_SETTING.message,
                    long_message=ParametersParseException.INTERLEAVER_SETTING.long_message,
                )
        return answer

    def reestablish(self, information: List[int]) -> List[int]:
        log.debug("Used Un Interleaver for package {0}".format(information))
        answer: List[int] = [0] * len(information)
        # noinspection PyBroadException
        try:
            # целочисленное деление с округлением вверх
            res_div: int = math.ceil(len(information) / self.lengthSmashing)
            for x in range(self.lengthSmashing):
                for y in range(res_div):
                    if len(information) > x * res_div + y:
                        answer[x + y * self.lengthSmashing] = information[x * res_div + y]
        except IndexError:
            if len(information) % self.lengthSmashing != 0:
                raise ParametersParseException(
                    message=ParametersParseException.INTERLEAVER_SETTING.message,
                    long_message=ParametersParseException.INTERLEAVER_SETTING.long_message,
                )

        return answer
