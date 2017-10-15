from abc import ABCMeta


class Coder:
    __metaclass__ = ABCMeta

    codingInformation: int = 0
    count_additional: int = 0
    n: int = 0
    k: int = 0

    def Encoding(self, information: int or list) -> list:
        pass

    def Decoding(self, information: list) -> list:
        pass

    def GetRedundancy(self) -> int:
        return int(self.count_additional / self.k * 100)

    def GetSpeed(self) -> float:
        return 1
