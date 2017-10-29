import itertools

import numpy as np

from coders import abstractCoder
from coders.casts import BitListToInt, IntToBitList


class Coder(abstractCoder.Coder):
    matrix_G: np.matrix
    vectors: list
    vectors_rise: list = []
    r: int
    power: int

    def __init__(self, power: int, r: int):
        self.r = r
        self.power = power

        init_matrix: list = [IntToBitList((1 << (1 << power)) - 1)]
        if r > 0:
            self.vectors = np.matrix([IntToBitList(x, size=power, rev=False) for x in range(2 ** power)]).T.tolist()
            init_matrix += self.vectors
            matrix_int_G1 = [BitListToInt(x) for x in init_matrix[1:]]
            self.vectors_rise = [[x] for x in range(1, power + 1)]

        for x in range(r - 1):
            comb: list = list(itertools.combinations(range(power), x + 2))

            new_matrix_G: list = []
            self.vectors_rise += comb
            for x in comb:
                val: int = matrix_int_G1[x[0]]
                for y in x:
                    val &= matrix_int_G1[y]
                new_matrix_G.append(IntToBitList(val, size=1 << power))
            init_matrix += new_matrix_G

        self.matrix_G = np.matrix(init_matrix)

    def Encoding(self, information: list):
        return [x % 2 for x in (np.matrix(information) * self.matrix_G).tolist()[0]]
        pass

    def Decoding(self, information: list):
        vec_sum = lambda a, b: [a[x] ^ b[x] for x in range(len(a))]
        vec_mul = lambda a, b: [a[x] & b[x] for x in range(len(a))]
        vec_inv = lambda a: [x ^ 1 for x in a]

        for x in range(len(self.matrix_G), 0, -1):
            voice: int = 0
            for option_mul in range(1 << len(self.vectors_rise[x])):
                pass
            pass

        pass
        #
        # [1111011011011000]
        # [1111101001101100]
