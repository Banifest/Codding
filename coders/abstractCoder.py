from abc import ABCMeta


class Coder:
    __metaclass__ = ABCMeta
    lengthInformation = 0
    lengthAdditional = 0
    lengthTotal = 0
    codingInformation = 0


    def GetRedundancy(self) -> int:
        return int(self.lengthAdditional / self.lengthInformation * 100)
