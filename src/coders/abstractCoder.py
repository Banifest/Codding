from abc import ABCMeta


class Coder:
    __metaclass__ = ABCMeta
    lengthInformation: int = 0
    lengthAdditional: int = 0
    lengthTotal: int = 0
    codingInformation: int = 0

    def Encoding(self, information: int or list) -> list:
        pass

    def Decoding(self, information: list) -> list:
        pass

    def GetRedundancy(self) -> int:
        return int(self.lengthAdditional / self.lengthInformation * 100)

    def GetSpeed(self) -> float:
        return 1
