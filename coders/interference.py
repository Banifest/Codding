import sys, os
from random import random

from coders.casts import IntToBitList, BitListToInt


def GenInterference(info: int, straight: float)->int:
    info = IntToBitList(info)
    answer = []
    for x in info:
        if random.random()<= straight:
            answer.append(int(x*(random.random()+0.5)))
    return BitListToInt(answer)