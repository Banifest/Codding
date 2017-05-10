import math

from src.coders import abstractCoder
from src.coders.casts import BitListToInt, IntToBitList
from src.coders.exeption import DecodingException


generatingPalindromes = [None, None, 0x7, 0xB, 0x29, 0x43, 0x89, 0x1D7]


class Coder(abstractCoder.Coder):
    polynomial = []

    def __init__(self, informationLength: int):
        self.lengthInformation = informationLength
        self.lengthAdditional = int(math.log2(informationLength - 1) + 2)
        self.polynomial = IntToBitList(generatingPalindromes[self.lengthAdditional])


    def GetRemainder(self, number: int, flag: bool = None) -> list:
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
        return [0 for x in range(0, self.lengthAdditional - int(math.log2(number)) - 1)] + IntToBitList(
                number) if number != 0 else [0]


    def Encoder(self, information: int) -> list:
        return IntToBitList(information) + self.GetRemainder(information, True)


    def Decoder(self, information: list) -> int:
        if BitListToInt(self.GetRemainder(BitListToInt(information), False)) == 0:
            return BitListToInt(information[:-self.lengthAdditional])
        else:
            count = 1
            while BitListToInt(self.GetRemainder((BitListToInt(information) << count), False)) != 0:
                count += 1
                if count > 100:
                    raise DecodingException("Не далось исправить ошибку")
            information[count + 1] = information[count + 1] % 2
            return BitListToInt(information[:-self.lengthAdditional])
