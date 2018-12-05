# coding=utf-8
# coding=utf-8
import math

import numpy as np
from numpy.polynomial import polynomial as plm

from src.coders import abstract_coder
from src.coders.casts import int_to_bit_list
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType


class Coder(abstract_coder.AbstractCoder):
    def get_coder_parameters(self):
        pass

    _name = "Циклический"
    polynomial: plm.Polynomial
    type_of_coder = EnumCodersType.CYCLICAL
    matrix_G: np.matrix  # порождающая матрица
    matrix_H: np.matrix  # проверочная матрицал

    def __init__(self, information_length: int, polynomial: int):
        log.debug("Создание циклического кодера")

        self.lengthInformation = information_length
        self.lengthAdditional = int(math.log2(polynomial))
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        self.polynomial = plm.Polynomial(int_to_bit_list(polynomial, rev=True))

    def encoding(self, information: list):
        mod: plm.Polynomial = plm.Polynomial([0] * self.lengthAdditional + information) % self.polynomial
        return [int(x) % 2 for x in mod] + [0] * (self.lengthAdditional - len(mod)) + information

    def decoding(self, information: list):
        syndrome: plm.Polynomial = plm.Polynomial(information) % self.polynomial
        for x in range(len(self.polynomial)):
            if sum([int(x) % 2 for x in syndrome]) != 0:
                arr_error: list = [int(x) % 2 for x in syndrome]
                for iter in range(len(arr_error)):
                    if arr_error[iter] != 0:
                        information[iter] ^= 1
            else:
                break

        return information[self.lengthAdditional:]

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    def get_speed(self) -> float:
        return super().get_speed()

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    def to_json(self) -> dict:
        return {'name'                   : self.name,
                'length information word': self.lengthInformation,
                'length additional bits' : self.lengthAdditional,
                'length coding word'     : self.lengthTotal,
                'polynomial'             : [int(x) for x in self.polynomial],
                'speed'                  : self.get_speed()}
