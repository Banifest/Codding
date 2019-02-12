# coding=utf-8
# coding=utf-8
from src.logger import log


class Interleaver:
    lengthSmashing: int

    def __init__(self, length_smashing: int):
        self.lengthSmashing = length_smashing

    def shuffle(self, information: list) -> list:
        log.debug("Используется перемежитель для пакета {0}".format(information))
        answer: list = []
        for x in range(self.lengthSmashing):
            is_end: bool = False
            counter: int = 0
            while not is_end:
                if (counter * self.lengthSmashing + x) < len(information):
                    answer.append(information[counter * self.lengthSmashing + x])
                else:
                    is_end = True
                counter += 1
        return answer

    def reestablish(self, information: list) -> list:
        log.debug("Используется деперемежитель для пакета {0}".format(information))
        answer: list = [0] * len(information)
        res_div: int = ((len(information) - 1) // self.lengthSmashing) + 1  # целочисленное деление с округлением вверх
        for x in range(self.lengthSmashing):
            for y in range(res_div):
                if len(information) > x * res_div + y:
                    answer[x + y * self.lengthSmashing] = information[x * res_div + y]

        return answer
