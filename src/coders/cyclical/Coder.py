import math

import numpy as np
from numpy.polynomial import polynomial as plm

from coders.exeption import CodingException
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
        self.lengthAdditional = int(math.log2(information_length - 1) + 2)
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

        self.polynomial = plm.Polynomial(IntToBitList(polynomial, rev=True))

        if sum([int(x) % 2 for x in
                plm.Polynomial([-1] + [0] * (information_length - 2) + [1]) / self.polynomial]) != 0:
            raise CodingException("Не верный полином")

        init_matrix: list = []
        column: list = IntToBitList(polynomial, rev=True) + [0] * self.lengthAdditional

        for x in range(self.lengthTotal - 1, self.lengthAdditional - 1, -1):
            init_matrix.append([int(x) % 2 for x in (plm.Polynomial(IntToBitList(1 << x, rev=True)) % self.polynomial)])

        for x in init_matrix:
            x += (self.lengthAdditional - len(x)) * [0]

        init_H_matrix: list = np.matrix(init_matrix).T.tolist()
        for x in range(self.lengthInformation):  # генерация единичной матрицы
            init_matrix[x] = [0] * x + [1] + [0] * (self.lengthInformation - x - 1) + init_matrix[x]

        self.matrix_G = np.matrix(init_matrix)

        for x in range(self.lengthAdditional):  # генерация единичной матрицы
            init_H_matrix[x] += [0] * x + [1] + [0] * (self.lengthAdditional - x - 1)

        self.matrix_H = np.matrix(init_H_matrix)

    def Encoding(self, information: list):
        information.reverse()
        additional_bits: list = [int(x) % 2 for x in
                                 (plm.Polynomial(information + [0] * self.lengthAdditional) % self.polynomial)]
        return information + [0] * (self.lengthAdditional - len(additional_bits)) + additional_bits
        pass
        # return [x % 2 for x in (np.matrix(information) * self.matrix_G.A).tolist()[0]]

    def Decoding(self, information: list):
        syndrome: int = sum([x % 2 for x in (np.matrix(information) * self.matrix_H.T).tolist()[0]])
        if syndrome != 0:
            print(syndrome)
        else:
            return information[:self.lengthInformation]