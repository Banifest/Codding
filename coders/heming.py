import sys, os, numpy as np, math
from coders.combinations import GetCombinations
from coders.casts import *

class Coder():
    lengthInformation = 0
    lengthAdditional = 0
    lengthTotal = 0
    codingInformation = 0

    def __init__(self, info: int):
        self.lengthAdditional = int(math.log2(info)) + 1
        self.lengthInformation = info
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

    def Encoding(self, info: int)->int:
        comb_list = GetCombinations(self.lengthAdditional + 1, self.lengthAdditional)
        count = 0
        answer = 0
        for x in comb_list[:self.lengthAdditional]:
            xor_one_comb = 0
            temp_info = IntToBitList(info)
            for y in [temp_info[y] for y in x]:
                xor_one_comb ^= y
            answer += (1 << count) * xor_one_comb
            count += 1

        answer += (info << count)
        return answer

    def Decoding(self, info: int)->int:
        comb_list = GetCombinations(self.lengthAdditional + 1, self.lengthAdditional)
        count = 0
        answer = 0
        for x in comb_list[:self.lengthAdditional]:
            xor_one_comb = 0
            temp_info = IntToBitList(info)
            k = [temp_info[y] for y in x]
            k.append(temp_info[-(count+1)])
            for y in k:
                xor_one_comb ^= y
            if xor_one_comb != 0:
                raise Exception("lol")
            count += 1
        return info >> self.lengthAdditional
