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
        self.lengthAdditional = int(math.log2(information_length - 1) + 2)
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

        # TODO добавить проверку на корректность введенной пользователем информации X^N - 1 должно делиться без
        # остатка на полином по модулю 2

        self.polynomial = plm.Polynomial(IntToBitList(polynomial, rev=True))
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
        return [x % 2 for x in (np.matrix(information) * self.matrix_G.A).tolist()[0]]

    def Decoding(self, information: list):
        syndrome: int = sum([x % 2 for x in (np.matrix(information) * self.matrix_H.T).tolist()[0]])
        if syndrome != 0:
            pass
        else:
            return information[:self.lengthInformation]
"""
    def __init__(self, information_length: int, polynomial: int = None):
        log.debug("Создание циклического кодера")
        self.lengthInformation = information_length
        self.lengthAdditional = int(math.log2(information_length - 1) + 1)
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        if polynomial is not None:
            self.polynomial = IntToBitList(polynomial)
        else:
            self.polynomial = IntToBitList(generatingPalindromes[self.lengthAdditional])

    def get_mod(self, information: int, flag: bool = False) -> list:
        polynomial = BitListToInt(self.polynomial)
        if flag:
            information <<= self.lengthAdditional

        while information != 0 and int(math.log2(polynomial)) <= int(math.log2(information)):
            distance = int(math.log2(information)) - int(math.log2(polynomial))
            temp_palindrome = polynomial << distance
            # операция деления
            temp_number = (information ^ temp_palindrome) &\
                          (((1 << int(math.log2(information) + 1)) - 1) ^ ((1 << distance) - 1))
            temp_number += ((1 << distance) - 1) & information
            information = temp_number
        return [0 for x in range(0, self.lengthAdditional - int(math.log2(information)) - 1)] + IntToBitList(
                information)\
            if information != 0 else [0]

    def Encoding(self, information: list) -> list:
        log.info("Кодирование пакета {0} циклическим кодером".format(information))
        return information + self.get_mod(BitListToInt(information), True)

    def Decoding(self, information: list) -> list:
        log.info("Декодирование пакета {0} циклическим декодером".format(information))
        if BitListToInt(self.get_mod(BitListToInt(information), False)) == 0:
            log.debug("Ошибка в пакете не обнаружена")
            return information[:-self.lengthAdditional]
        else:
            count: int = 1
            log.debug("Обнаружена ошибка в пакете")
            while BitListToInt(self.get_mod((BitListToInt(information) << count), False)) != 0:
                count += 1
                if count > 100:
                    log.debug("Не далось исправить ошибку")
                    raise DecodingException("Не далось исправить ошибку")
            return (information[count + 1] % 2)[:-self.lengthAdditional]
"""
