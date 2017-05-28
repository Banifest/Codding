import math

from src.coders import abstractCoder
from src.coders.casts import BitListToInt, IntToBitList
from src.coders.exeption import DecodingException
from src.logger import log


generatingPalindromes = [None, None, 0x7, 0xB, 0x29, 0x43, 0x89, 0x1D7]


class Coder(abstractCoder.Coder):
    polynomial: list = []

    def __init__(self, informationLength: int, polynomial: int = None):
        log.debug("Создание циклического кодера")
        self.lengthInformation = informationLength
        self.lengthAdditional = int(math.log2(informationLength - 1) + 1)
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        if polynomial is not None:
            self.polynomial = IntToBitList(polynomial)
        else:
            self.polynomial = IntToBitList(generatingPalindromes[self.lengthAdditional])


    def GetRemainder(self, number: int, flag: bool = False) -> list:
        polynomial = BitListToInt(self.polynomial)
        if flag:
            number <<= self.lengthAdditional

        while number != 0 and int(math.log2(polynomial)) <= int(math.log2(number)):
            distance = int(math.log2(number)) - int(math.log2(polynomial))
            tempPalindrome = polynomial << distance
            # операция деления
            tempNumber = (number ^ tempPalindrome) &\
                         (((1 << int(math.log2(number) + 1)) - 1) ^ ((1 << distance) - 1))
            tempNumber += ((1 << distance) - 1) & number
            number = tempNumber
        return [0 for x in range(0, self.lengthAdditional - int(math.log2(number)) - 1)] + IntToBitList(number)\
            if number != 0 else [0]


    def Encoding(self, information: list) -> list:
        log.info("Кодирование пакета {0} циклическим кодером".format(information))
        return information + self.GetRemainder(BitListToInt(information), True)


    def Decoding(self, information: list) -> list:
        log.info("Декодирование пакета {0} циклическим декодером".format(information))
        if BitListToInt(self.GetRemainder(BitListToInt(information), False)) == 0:
            log.debug("Ошибка в пакете не обнаружена")
            return BitListToInt(information[:-self.lengthAdditional])
        else:
            count = 1
            log.debug("Обнаружена ошибка в пакете")
            while BitListToInt(self.GetRemainder((BitListToInt(information) << count), False)) != 0:
                count += 1
                if count > 100:
                    log.debug("Не далось исправить ошибку")
                    raise DecodingException("Не далось исправить ошибку")
            information[count + 1] = information[count + 1] % 2
            return information[:-self.lengthAdditional]