import math

import numpy as np
from numpy.polynomial import polynomial as plm

from src.coders import abstractCoder
from src.coders.casts import IntToBitList
from src.logger import log


generatingPalindromes = [None, None, 0x7, 0xB, 0x29, 0x43, 0x89, 0x1D7]


class Coder(abstractCoder.Coder):
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
        if sum([int(x) % 2 for x in syndrome]) != 0:
            arr_error: list = [int(x) % 2 for x in syndrome]
            for x in range(len(arr_error)):
                if arr_error[x] != 0:
                    information[x] ^= 1
        else:
            return information[self.lengthAdditional:]
