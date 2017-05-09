import random

import coders
from coders.casts import BitListToInt, IntToBitList


class Coder(coders.abstractCoder.Coder):
    countCodingBlocks: int  # количество блоков информации
    countBlocks: int  # количество блоков сочетаний
    sizeBlock: int  # Размер одного блока
    blocks: list  # блоки сочетаний

    def __init__(self, sizeBlock: int, countCodingBlocks: int, lengthInformation: int):
        self.sizeBlock = sizeBlock
        self.blocks = []
        self.countCodingBlocks = countCodingBlocks
        self.countBlocks = ((lengthInformation - 1) // self.sizeBlock) + 1  # целочисленное деление с округлением вверх

        randomGenerator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел
        # Генерация блоков сочетаний
        setCombinationBlocks: set = set()
        while len(setCombinationBlocks) < self.countCodingBlocks:
            setCombinationBlocks.add(randomGenerator.getrandbits(self.countBlocks))
            setCombinationBlocks = setCombinationBlocks - {0}
        self.blocks: list = list(setCombinationBlocks)

    def Encoding(self, information: list):
        combinationBlocks: list = []
        for x in range(0, len(information), self.sizeBlock):
            combinationBlocks.append(BitListToInt(information[x:min(x + self.sizeBlock, len(information))]))

        answer: list = []

        for x in range(self.countCodingBlocks):
            value: int = 0
            count: int = 0
            for y in IntToBitList(self.blocks[x], self.countBlocks):
                if y == 1:
                    value ^= combinationBlocks[count]
                count += 1
            answer.append(IntToBitList(value, self.sizeBlock))

        return [y for x in answer for y in x]



    def Decoding(self, information: list):
        decodedSet: set = set()
        isKill: bool = False

        # Разбивка на блоки
        stastus: list = []
        for x in range(0, len(information), self.sizeBlock):
            tempList: list = []
            for y in range(len(self.sizeBlock)):
                if (x + y) < len(information):
                    tempList.append(information[x + y])

        while not isKill:
            isKill = True
