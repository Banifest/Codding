import math

from coders.abstractCoder import Coder
from coders.casts import BitListToInt, IntToBitList


class Coder(Coder):
    countPolynomials = 0
    listPolynomials = []
    countInput = 0
    countOutput = 0
    countRegisters = 0
    register = 0

    def __init__(self, countPolynomials: int, listPolynomials: list, countInput: int, countOutput: int,
                 countRegister: int):
        self.countInput = countInput
        self.countOutput = countOutput
        self.countRegisters = countRegister
        self.countPolynomials = countPolynomials
        self.listPolynomials = listPolynomials
        # self.registers = [0 for x in range(countRegister)]


    def DoStep(self, informationBit) -> int:
        self.register >>= 1
        # зануление старшего бита
        self.register = self.register & ((1 << (int(math.log2(self.register)))) - 1)
        self.register += informationBit

        answer = []
        power = 0
        for count in range(self.countPolynomials):
            addedBit = 0
            for x in IntToBitList(self.listPolynomials[count] & self.register):
                addedBit ^= x * (1 << power)
            answer.append(addedBit)
            power += 1

        return BitListToInt(answer)
