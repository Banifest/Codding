import math

import numpy as np
from numpy.polynomial import polynomial as plm

from coders.exeption import CodingException
from src.coders import abstractCoder
from src.coders.casts import IntToBitList
from src.logger import log


class Coder(abstractCoder.AbstractCoder):
    name = "Циклический"
    polynomial: plm.Polynomial
    matrix_G: np.matrix  # порождающая матрица
    matrix_H: np.matrix  # проверочная матрицал

    def __init__(self, information_length: int, polynomial: int):
        log.debug("Создание циклического кодера")

        self.lengthInformation = information_length
        self.lengthAdditional = int(math.log2(polynomial))
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        self.polynomial = plm.Polynomial(IntToBitList(polynomial, rev=True))

    def Encoding(self, information: list):
        mod: plm.Polynomial = plm.Polynomial([0] * self.lengthAdditional + information) % self.polynomial
        return [int(x) % 2 for x in mod] + [0] * (self.lengthAdditional - len(mod)) + information

    def Decoding(self, information: list):
        syndrome: plm.Polynomial = plm.Polynomial(information) % self.polynomial
        for x in range(len(self.polynomial)):
            if sum([int(x) % 2 for x in syndrome]) != 0:
                arr_error: list = [int(x) % 2 for x in syndrome]
                for x in range(len(arr_error)):
                    if arr_error[x] != 0:
                        information[x] ^= 1
            else:
                break

        return information[self.lengthAdditional:]

    def get_redundancy(self) -> float:
        pass

    def get_speed(self) -> float:
        return self.lengthAdditional / self.lengthTotal

    def try_normalization(self, bit_list: list) -> list:
        if len(bit_list) > self.lengthInformation:
            raise CodingException("Невозможно привести информационное слово с большей длиной к меньшему")
        else:
            return (self.lengthInformation - len(bit_list)) * [0] + bit_list
