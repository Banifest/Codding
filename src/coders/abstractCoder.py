from abc import ABCMeta


class Coder:
    __metaclass__ = ABCMeta

    coding_information: int = 0
    count_additional: int = 0
    lengthTotal: int = 0
    lengthInformation: int = 0

    def Encoding(self, information: int or list) -> list:
        pass

    def Decoding(self, information: list) -> list:
        pass

    def GetRedundancy(self) -> int:
        return int(self.count_additional / self.lengthInformation * 100)

    def GetSpeed(self) -> float:
        return self.lengthInformation / self.lengthTotal * 100
