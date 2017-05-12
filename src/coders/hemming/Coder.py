import numpy as np

from src.coders import abstractCoder
from src.coders.casts import *
from src.coders.exeption import DecodingException


class Coder(abstractCoder.Coder):
    arr: list = []

    def __init__(self, lengthInformation: int):
        self.lengthAdditional = int(math.log2(lengthInformation - 1) + 2)
        self.lengthInformation = lengthInformation
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

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
            self.arr.append(temp)
        self.arr = np.transpose(np.array(self.arr))

    def Encoding(self, information: int) -> list:
        listEncodingInformation = IntToBitList(information)
        listEncodingInformation.reverse()
        if len(listEncodingInformation) < self.lengthInformation:
            for x in range(self.lengthInformation - len(listEncodingInformation)):
                listEncodingInformation.append(0)
        listEncodingInformation.reverse()
        code: list = []

        for count in range(self.lengthTotal):
            if math.log2(count + 1) == int(math.log2(count + 1)):  # Проверка кратности числа на степень 2х
                code.append([0])
            else:
                code.append([listEncodingInformation[count - int(math.log2(count)) - 1]])

        answer = [x[0] for x in code]
        code = np.transpose(np.array(code))
        backup_info = list((np.dot(code, self.arr) % 2)[0])
        for x in range(self.lengthAdditional):
            answer[((1 << x) - 1)] = backup_info[x]
        return answer


    def Decoding(self, info: list) -> list:
        code = np.transpose(np.array([[x] for x in info]))
        answer: list = []
        status: list = list((np.dot(code, self.arr) % 2)[0])
        status.reverse()
        status: int = BitListToInt(status)
        if status != 0:
            code[0][status - 1] = (code[0][status - 1] + 1) % 2
            oldStatus = status
            status = BitListToInt(list((np.dot(code, self.arr) % 2)[0]))
            if status != 0:
                print(status)
                raise DecodingException("Не удалось успешно исправить обнаруженные ошибки")
            print("Произошло успешное исправление ошибки в бите под номером {0}".format(oldStatus))
        for count in range(len(code[0])):
            if math.log2(count + 1) != int(math.log2(count + 1)):
                answer.append(code[0][count])
        return answer
