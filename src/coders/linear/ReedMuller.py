import itertools

import numpy as np

from coders import abstractCoder
from coders.casts import BitListToInt, IntToBitList


class Coder(abstractCoder.Coder):
    matrix_G: np.matrix

    def __init__(self, power: int, r: int):
        init_matrix: list = [IntToBitList((1 << (1 << power)) - 1)]
        init_matrix += np.matrix([IntToBitList(x, size=power) for x in range(2 ** power)]).T.tolist()
        matrix_int_G1 = [BitListToInt(x) for x in init_matrix[1:]]

        for x in range(r):
            comb: list = list(itertools.combinations(range(power), x + 2))

            new_matrix_G: list = []
            for x in comb:
                val: int = matrix_int_G1[x[0]]
                for y in x:
                    val &= matrix_int_G1[y]
                new_matrix_G.append(IntToBitList(val, size=1 << power))
            init_matrix += new_matrix_G

        self.matrix_G = np.matrix(init_matrix)
