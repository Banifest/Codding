import math

from coders import abstractCoder
from coders.casts import BitListToInt, IntToBitList


generatingPalindromes = [None, None, 0x7, 0xB, 0x29, 0x43, 0x89, 0x1D7]


class Coder(abstractCoder.Coder):
    palindrome = []

    def __init__(self, informationLength: int):
        self.lengthInformation = informationLength
        self.lengthAdditional = int(math.log2(informationLength - 1) + 2)
        self.palindrome = IntToBitList(generatingPalindromes[self.lengthAdditional])


    def GetRemainder(self, number: int) -> list:
        palindrome = BitListToInt(self.palindrome)
        number <<= self.lengthAdditional
        while int(math.log2(palindrome)) <= int(math.log2(number)):
            distance = int(math.log2(number)) - int(math.log2(palindrome))
            tempPalindrome = palindrome << distance
            # операция деления
            tempNumber = (number ^ tempPalindrome) &\
                         (((1 << int(math.log2(number) + 1)) - 1) ^ ((1 << distance) - 1))
            tempNumber += ((1 << distance) - 1) & number
            number = tempNumber
        return [0 for x in range(0, self.lengthAdditional - int(math.log2(number)) - 1)] + IntToBitList(number)


    def Encoder(self, information: int) -> list:
        return IntToBitList(information) + self.GetRemainder(information)


    def Decoder(self, information):
        pass
