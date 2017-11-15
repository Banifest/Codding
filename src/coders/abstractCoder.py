from abc import ABCMeta, abstractmethod


class AbstractCoder:
    __metaclass__ = ABCMeta

    name: str = ""
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
        return self.count_additional / self.lengthInformation

    @abstractmethod
    def GetSpeed(self) -> float:
        return self.lengthInformation / self.lengthTotal
