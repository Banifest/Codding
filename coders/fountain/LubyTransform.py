import random

import coders
from coders.casts import BitListToInt, BitListToIntList, IntToBitList


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
        decodedSetList: list = [set(BitListToIntList(IntToBitList(x, self.sizeBlock))) for x in self.blocks]
        decodedSetList.append(set())  # костыль, чтобы работало
        isKill: bool = False

        # Разбивка на блоки
        status: list = [False for x in range(self.countBlocks)]
        status.append(True)  # костыль, чтобы работало

        tempList: list = []
        for x in range(0, len(information), self.sizeBlock):
            temp: list = []
            for y in range(self.sizeBlock):
                if (x + y) < len(information):
                    temp.append(information[x + y])
            tempList.append(BitListToInt(temp))
        tempList.append(0)  # костыль, чтобы работало

        answer: list = [0] * self.countCodingBlocks
        while not isKill or {True} != set(status):
            isKill = True
            for x in range(len(decodedSetList)):
                for y in range(len(decodedSetList)):
                    difference = decodedSetList[x] - decodedSetList[y]
                    if len(difference) == 1 and (decodedSetList[y] - decodedSetList[x]) == set():
                        isKill = False
                        status[list(difference)[0]] = True
                        answer[list(difference)[0]] = tempList[x] ^ tempList[y]
                        for z in range(len(decodedSetList)):
                            if list(difference)[0] in decodedSetList[z]:
                                tempList[z] ^= answer[list(difference)[0]]
                                decodedSetList[z] = decodedSetList[z] - difference

        # формирование отвера в битовом представлении
        answer = answer[:-1]
        answer.reverse()
        answer = [IntToBitList(x, self.sizeBlock) for x in answer]
        return [y for x in answer for y in x]
