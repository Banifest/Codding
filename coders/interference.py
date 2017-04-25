import sys, os
from random import random

from coders.casts import IntToBitList, BitListToInt


def GenInterference(info: list, straight: float) -> list:
    answer = []
    for x in info:
        if random() <= straight:
            answer.append(x * int(random() + 0.5))
        else:
            answer.append(x)
    return answer
