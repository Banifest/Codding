from src.logger import log


class Interleaver:
    lengthSmashing: int

    def __init__(self, lengthSmashing: int):
        self.lengthSmashing = lengthSmashing

    def shuffle(self, information: list) -> list:
        log.debug("Используется перемежитель для пакета {0}".format(information))
        answer: list = []
        for x in range(self.lengthSmashing):
            isEnd: bool = False
            counter: int = 0
            while not isEnd:
                if (counter * self.lengthSmashing + x) < len(information):
                    answer.append(information[counter * self.lengthSmashing + x])
                else:
                    isEnd = True
                counter += 1
        return answer

    def reestablish(self, information: list) -> list:
        log.debug("Используется деперемежитель для пакета {0}".format(information))
        answer: list = [0] * len(information)
        resDiv: int = ((len(information) - 1) // self.lengthSmashing) + 1  # целочисленное деление с округлением вверх
        for x in range(self.lengthSmashing):
            for y in range(resDiv):
                if len(information) > x * resDiv + y:
                    answer[x + y * self.lengthSmashing] = information[x * resDiv + y]

        return answer
