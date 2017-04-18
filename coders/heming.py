import sys, os, numpy as np, math
from coders.combinations import GetCombinations
from coders.casts import *
from coders.exeption import DecodingException


class Coder():
    lengthInformation = 0
    lengthAdditional = 0
    lengthTotal = 0
    codingInformation = 0
    arr = []

    def __init__(self, info: int):
        self.lengthAdditional = int(math.log2(info)) + 1
        self.lengthInformation = info
        self.lengthTotal = self.lengthInformation + self.lengthAdditional

        for x in range(self.lengthAdditional):
            temp = []
            count = 0
            flag = True
            for y in range(x):
                count += 1

            for y in range(x):
                temp.append(0)

            while count < self.lengthTotal:
                for y in range(x + 1):
                    temp.append(1) if flag == True else temp.append(0)
                    count += 1
                    if count >= self.lengthTotal:
                        break
                flag = not flag
            self.arr.append(temp)


        self.arr = np.transpose(np.array(self.arr))

    def Encoding(self, info: int) -> list:
        temp = IntToBitList(info)
        temp.reverse()
        code = []
        """code = [
            code.append([0]) if math.log2(count + 1) == int(math.log2(count + 1))\
                else code.append([temp[count - int(math.log2(count)) - 1]])\
            for count in range(self.lengthTotal)
            ]
        """
        for count in range(self.lengthTotal):
            if math.log2(count + 1) == int(math.log2(count + 1)):
                code.append([0])
            else:
                code.append([temp[count - int(math.log2(count)) - 1]])

        answer = [x[0] for x in code]
        code = np.transpose(np.array(code))
        backup_info = list((np.dot(code, self.arr) % 2)[0])
        for x in range(self.lengthAdditional):
            answer[((1 << x)-1)] = backup_info[x]
        return answer
        """comb_list = GetCombinations(self.lengthAdditional + 1, self.lengthAdditional)
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
"""

    def Decoding(self, info: list) -> int:
        code = np.transpose(np.array([[x] for x in info]))
        answer = []
        status = BitListToInt(list((np.dot(code, self.arr) % 2)[0]))
        if status != 0:
            print(status)
            raise DecodingException()
        for count in range(len(code[0])):
            if  math.log2(count + 1) != int(math.log2(count + 1)):
                answer.append(code[0][count])
        return BitListToInt(answer)