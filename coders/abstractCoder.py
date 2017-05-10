from abc import ABCMeta


class Coder:
    __metaclass__ = ABCMeta
    lengthInformation: int = 0
    lengthAdditional: int = 0
    lengthTotal: int = 0
    codingInformation: int = 0


    def GetRedundancy(self) -> int:
        return int(self.lengthAdditional / self.lengthInformation * 100)
