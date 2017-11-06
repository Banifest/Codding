from abc import ABCMeta, abstractmethod


class Coder:
    __metaclass__ = ABCMeta

    coding_information: int = 0
    count_additional: int = 0
    lengthTotal: int = 0
    lengthInformation: int = 0

    @abstractmethod
    def Encoding(self, information: int or list) -> list:
        pass

    @abstractmethod
    def Decoding(self, information: list) -> list:
        pass

    @abstractmethod
    def GetRedundancy(self) -> int:
        return int(self.count_additional / self.lengthInformation * 100)

    @abstractmethod
    def GetSpeed(self) -> float:
        return self.lengthInformation / self.lengthTotal * 100
