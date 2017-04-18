import sys, os, numpy as np

from coders import heming
from coders.combinations import GetCombinations
from coders.interference import GenInterference


if __name__ == '__main__':
    #  print(GetCombinations(4, 3))
    c = 'a'
    a = heming.Coder(4)
#    print(a.Encoding(11))
    print(a.Decoding(a.Encoding(11)))
    print(GenInterference(a.Encoding(13), 0.5))


else:
    pass
