from coders.interleaver.Interleaver import Interleaver


class Deinterleaver:
    lengthSmashing: int

    def __init__(self, lengthSmashing: int = None, interleaver: Interleaver = None):
        if lengthSmashing is not None:
            self.lengthSmashing = lengthSmashing
        if interleaver is not None:
            self.lengthSmashing = interleaver.lengthSmashing

    def Reestablish(self, information: list) -> list:
        answer: list = [0] * len(information)
        resDiv: int = ((len(information) - 1) // self.lengthSmashing) + 1  # целочисленное деление с округлением вверх
        for x in range(self.lengthSmashing):
            for y in range(resDiv):
                if len(information) > x * resDiv + y:
                    answer[x + y * self.lengthSmashing] = information[x * resDiv + y]

        return answer
