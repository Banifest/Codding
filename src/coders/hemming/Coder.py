import numpy as np

from src.coders import abstractCoder
from src.coders.casts import *
from src.coders.exeption import DecodingException
from src.logger import log


class Coder(abstractCoder.Coder):
    matrix_transformation: list = []

    def __init__(self, length_information: int):
        log.debug("Создание кодера хемминга")
        self.lengthAdditional = int(math.log2(length_information) + 1)
        self.lengthInformation = length_information
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        self.matrix_transformation = []

        for x in range(self.lengthAdditional):
            temp: list = []
            flag = True
            count = (1 << x) - 1  # Количество символов требуемых для зануления вначале
            for y in range((1 << x) - 1):
                temp.append(0)

            while count < self.lengthTotal:
                for y in range(1 << x):
                    temp.append(1) if flag == True else temp.append(0)
                    count += 1
                    if count >= self.lengthTotal:
                        break
                flag: bool = not flag
            self.matrix_transformation.append(temp)
        self.matrix_transformation = np.transpose(np.array(self.matrix_transformation))

    def GetSpeed(self) -> float:
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
            if math.log2(count + 1) != int(
                    math.log2(count + 1)) or step >= self.lengthAdditional:  # Проверка кратности числа на степень 2х
                code.append([list_encoding_information[count - int(math.log2(count)) - 1]])
            else:
                code.append([0])
                step += 1

        answer = [x[0] for x in code]
        code = np.transpose(np.array(code))
        backup_info = list((np.dot(code, self.matrix_transformation) % 2)[0])
        for x in range(self.lengthAdditional):
            answer[(1 << x) - 1] = backup_info[x]
        return answer

    def Decoding(self, information: list) -> list:
        log.info("Декодирование пакета {0} декодером хемминга".format(information))

        code = np.transpose(np.array([[x] for x in information]))
        answer: list = []
        status: list = list((np.dot(code, self.matrix_transformation) % 2)[0])
        status.reverse()
        status: int = BitListToInt(status)
        if status != 0:
            log.debug("Обнаруженна(ы) ошибка(и)")

            if len(code[0]) > status - 1:
                code[0][status - 1] = (code[0][status - 1] + 1) % 2
                old_status = status
                status = BitListToInt(list((np.dot(code, self.matrix_transformation) % 2)[0]))

                if status != 0:
                    log.debug("Не удалось успешно исправить обнаруженные ошибки")
                    raise DecodingException("Не удалось успешно исправить обнаруженные ошибки")
                log.debug("Произошло успешное исправление ошибки в бите под номером {0}".format(old_status))
            else:
                log.debug("Не удалось успешно исправить обнаруженные ошибки")
                raise DecodingException("Не удалось успешно исправить обнаруженные ошибки")
        count: int = 0
        step: int = 0
        for x in code[0]:
            if math.log2(count + 1) != int(math.log2(count + 1)) or step >= self.lengthAdditional:
                answer.append(x)
            else:
                step += 1
            count += 1
        return answer
