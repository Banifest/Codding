import random

from src.coders import abstractCoder
from src.coders.casts import BitListToInt, BitListToIntList, IntToBitList
from src.coders.exeption import CodingException
from src.logger import log


class Coder(abstractCoder.AbstractCoder):
    name = "Фонтанный"

    countCodingBlocks: int  # количество блоков информации
    countBlocks: int  # количество блоков сочетаний
    sizeBlock: int  # Размер одного блока
    blocks: list  # блоки сочетаний

    def __init__(self, size_block: int, count_coding_blocks: int, length_information: int):
        log.debug("Создание фонтанного кодера с параметрами:{0}, {1}, {2}".
                  format(size_block, count_coding_blocks, length_information))
        self.lengthInformation = length_information
        self.sizeBlock = size_block
        self.blocks = []
        self.countCodingBlocks = count_coding_blocks
        self.countBlocks = ((length_information - 1) // self.sizeBlock) + 1  # целочисленное деление с округлением вверх

        randomGenerator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел
        # Генерация блоков сочетаний
        setCombinationBlocks: set = set()
        while len(setCombinationBlocks) < self.countCodingBlocks:
            if 2 ** self.countBlocks - 1 == len(setCombinationBlocks):
                raise CodingException("Не возможно содат кодер с заданными параметрами")
            setCombinationBlocks.add(randomGenerator.getrandbits(self.countBlocks))
            setCombinationBlocks = setCombinationBlocks - {0}

        self.blocks: list = list(setCombinationBlocks)
        self.lengthInformation = length_information
        self.lengthAdditional = size_block * count_coding_blocks - length_information
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

    def Encoding(self, information: list):
        log.info("Кодирование пакета {0} фонтанным LT-кодером".format(information))
        combinationBlocks: list = []
        information = [0] * abs(len(information) - self.lengthInformation) + information  # добавление 0 битов вначало
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
        """
        Декодер LT-фонтанного кода с заранее установленным генератором случайных чисел
        :param information: list Закодированная информация, представленная в виде массива битов
        :return: list Декодированная информация, представленная в виде массива битов
        """
        log.info("Декодирование пакета {0} фонтанным LT-декодером".format(information))
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
        while not isKill and {True} != set(status):
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

        if set(status) != {True}:
            log.debug("Недостаточно блоков для декодирования информации")
            raise CodingException("Невозможно декодировать :'(")

        # формирование ответа в битовом представлении
        answer = answer[:-1]
        answer = [IntToBitList(answer[0])] + [IntToBitList(x, self.sizeBlock) for x in answer[1:]]
        answer.reverse()
        return [y for x in answer for y in x]

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    def get_speed(self) -> float:
        return super().get_speed()

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    def to_json(self) -> dict:
        return {'name'                   : self.name,
                'length information word': self.lengthInformation,
                'length additional bits' : self.lengthAdditional,
                'length coding word'     : self.lengthTotal,
                'speed'                  : self.get_speed()}
