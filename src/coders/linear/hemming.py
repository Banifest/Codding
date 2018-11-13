# coding=utf-8
# coding=utf-8
import math

import numpy as np

from src.coders import abstractCoder
from src.coders.casts import *
from src.logger import log
from src.statistics.db.coder import Coder


class Coder(abstractCoder.AbstractCoder):
    name = "Хемминга"
    type_of_coder = Coder.CodersType.HEMMING

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    _matrixTransformation: list = []

    def __init__(self, length_information: int):
        log.debug("Создание кодера хемминга")

        # sum (2**(n-1)-1) from 1 to n must be >= length_information for correct check
        for x in range(1, length_information):
            if 2 ** x - x - 1 >= length_information:
                self.lengthAdditional = x
                break

        self.lengthInformation = length_information
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        self._matrixTransformation = []

        for x in range(self.lengthAdditional):
            temp: list = []
            flag = True
            count = (1 << x) - 1  # Количество символов требуемых для зануления вначале
            for y in range((1 << x) - 1):
                temp.append(0)

            while count < self.lengthTotal:
                for y in range(1 << x):
                    temp.append(1) if flag else temp.append(0)
                    count += 1
                    if count >= self.lengthTotal:
                        break
                flag: bool = not flag
            self._matrixTransformation.append(temp)
        self._matrixTransformation = np.transpose(np.array(self._matrixTransformation))

    def get_speed(self) -> float:
        return float(self.lengthInformation) / float(self.lengthTotal)

    def Encoding(self, information: list) -> list:
        log.info("Кодирование пакета {0} кодером хемминга".format(information))
        list_encoding_information: list = information
        list_encoding_information.reverse()
        if len(list_encoding_information) < self.lengthInformation:
            for x in range(self.lengthInformation - len(list_encoding_information)):
                list_encoding_information.append(0)
        list_encoding_information.reverse()
        code: list = []

        step: int = 0
        for count in range(self.lengthTotal):  # добавление проверяющих битов

            # Проверка кратности числа на степень 2х
            if math.log2(count + 1) != int(math.log2(count + 1)) or step >= self.lengthAdditional:
                code.append([list_encoding_information[count - int(math.log2(count)) - 1]])
            else:
                code.append([0])
                step += 1

        answer = [x[0] for x in code]
        code = np.transpose(np.array(code))
        backup_info = list((np.dot(code, self._matrixTransformation) % 2)[0])
        for x in range(self.lengthAdditional):
            answer[(1 << x) - 1] = backup_info[x]
        return answer

    def Decoding(self, information: list) -> list:
        log.info("Декодирование пакета {0} декодером хемминга".format(information))

        code = np.transpose(np.array([[x] for x in information]))
        answer: list = []
        status: list = list((np.dot(code, self._matrixTransformation) % 2)[0])
        status.reverse()
        status: int = BitListToInt(status)
        if status != 0:
            log.debug("Обнаруженна(ы) ошибка(и)")

            if len(code[0]) > status - 1:
                code[0][status - 1] = (code[0][status - 1] + 1) % 2
                old_status = status
                status = BitListToInt(list((np.dot(code, self._matrixTransformation) % 2)[0]))

                if status != 0:
                    log.debug("Не удалось успешно исправить обнаруженные ошибки")
                    # raise CodingException("Не удалось успешно исправить обнаруженные ошибки")
                log.debug("Произошло успешное исправление ошибки в бите под номером {0}".format(old_status))
            else:
                log.debug("Не удалось успешно исправить обнаруженные ошибки")
                # raise CodingException("Не удалось успешно исправить обнаруженные ошибки")
        count: int = 0
        step: int = 0
        for x in code[0]:
            if math.log2(count + 1) != int(math.log2(count + 1)) or step >= self.lengthAdditional:
                answer.append(x)
            else:
                step += 1
            count += 1
        return answer

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'length information word': self.lengthInformation,
            'length additional bits': self.lengthAdditional,
            'length coding word': self.lengthTotal,
            'matrix of generating': self._matrixTransformation.tolist(),
            'speed': self.get_speed()
        }
