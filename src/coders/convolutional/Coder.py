from src.coders import abstractCoder
from src.coders.casts import BitListToInt, CycleShiftRightBitList, GetHemmingDistance, IntToBitList
from src.logger import log


class Coder(abstractCoder.Coder):
    countPolynomials: int = 0
    listPolynomials: list = []
    countInput: int = 0
    countOutput: int = 0
    countRegisters: int = 0
    register: int = 0

    graph: list = []

    def __init__(self, countPolynomials: int, listPolynomials: list, countInput: int, countOutput: int,
                 countRegister: int):
        log.debug("Создание свёрточного кодера ....")
        self.countInput = countInput
        self.countOutput = countOutput
        self.countRegisters = countRegister
        self.countPolynomials = countPolynomials
        self.listPolynomials = listPolynomials

        self.lengthInformation = 1
        self.lengthAdditional = 1

        self.graph = self.GetGraph()

    def GetSpeed(self):
        return 1 / self.countRegisters

    def DoStep(self, informationBit: int) -> list:
        log.debug("Шаг при кодировании бита - {0}".format(informationBit))
        self.register <<= 1

        # зануление старшего бита
        self.register = self.register & ((1 << (self.countRegisters + 1)) - 1)
        self.register += informationBit

        answer = []
        power = 0
        for count in range(self.countPolynomials):
            addedBit = 0
            for x in IntToBitList(self.listPolynomials[count] & self.register):
                addedBit ^= x
            answer.append(addedBit % 2)
            power += 1
        return answer

    def GetGraph(self) -> list:
        """
        Формирует список представляющий граф переходов, где каждая вершина
        [
        [номер вершины в которую переходим, [биты которые соответвуют переходу]],
        ...
        ]
        """
        answer: list = []
        for x in range(2 ** self.countRegisters):
            vertex: list = []
            self.register = x
            edge: list = IntToBitList(x, self.countRegisters)
            edge = CycleShiftRightBitList(edge)
            edge[0] = 0
            vertex.append([BitListToInt(edge), self.DoStep(0)])
            self.register = x
            edge[0] = 1
            vertex.append([BitListToInt(edge), self.DoStep(1)])
            answer.append(vertex)

        self.register = 0
        return answer


    def Encoding(self, information: list) -> list:
        log.info("Кодирование пакета {0} свёрточным кодером".format(information))
        information.reverse()
        answer = []
        for x in information:
            temp = self.DoStep(x)
            for y in temp:
                answer.append(y)
        return answer


    def Decoding(self, information: list):
        lastStep: list = []  # Информация об предыдущем шаге
        nowStep: list = []  # Информация о текущем шаге
        infoAboutVertex: list = []  # информация о вершине
        travel: list = []  # путь для текущей вершины
        costTravel: int = 0  # стоимость для текущего пути

        infoDividedIntoSteps: list = []  # информация поделенная на шаги
        for x in range(0, len(information), self.countOutput):
            count: int = 0
            tempList: list = []
            while count < self.countOutput:
                tempList.append(information[x + count])
                count += 1
            infoDividedIntoSteps.append(tempList)

        lastStep = nowStep = [[0, []]] + [[99999, []] for x in
                                          range(self.countRegisters ** 2 - 1)]  # заполняет первый шаг

        for x in infoDividedIntoSteps:
            nowStep = [[99999, []] for x in range(self.countRegisters ** 2)]  # заполняет первый шаг
            number: int = 0
            for infoAboutVertex in lastStep:
                vertexStep: int = self.graph[number][0][0]  # вершина перехода
                distance: int = GetHemmingDistance(x, self.graph[number][0][1])
                if nowStep[vertexStep][0] > lastStep[number][0] + distance:
                    nowStep[vertexStep] = [infoAboutVertex[0] + distance, infoAboutVertex[1] + self.graph[number][0][1]]

                vertexStep: int = self.graph[number][1][0]  # вершина перехода
                distance: int = GetHemmingDistance(x, self.graph[number][1][1])
                if nowStep[vertexStep][0] > lastStep[number][0] + distance:
                    nowStep[vertexStep] = [infoAboutVertex[0] + distance, infoAboutVertex[1] + self.graph[number][1][1]]

                number += 1
            lastStep = nowStep

        minAnswer: list = []
        minCost: int = 999999
        for x in lastStep:
            if minCost > x[0]:
                minCost = x[0]
                minAnswer = x[1]
        return minAnswer
