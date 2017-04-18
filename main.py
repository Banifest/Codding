import sys, os, numpy as np

from coders import heming
from coders.combinations import GetCombinations


if __name__ == '__main__':
    #  print(GetCombinations(4, 3))
    c = 'a'
    a = heming.Coder(4)
    print(a.Encoding(11))
    print(a.Decoding(a.Encoding(11)))


else:
    pass
