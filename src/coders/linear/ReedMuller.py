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
        vec_xor = lambda a, b: [a[x] ^ b[x] for x in range(len(a))]
        vec_mul = lambda a, b: [a[x] & b[x] for x in range(len(a))]
        vec_inv = lambda a: [x ^ 1 for x in a]

        result_voice: list = []
        for vector in self.matrix_G.tolist()[1::-1]:
            voice: int = 1  # голосовалка

            # проверка на ортогональность
            orthogonal_vectors: list = [vector]
            for test_vector in self.matrix_G.tolist()[1:]:
                for x in orthogonal_vectors:
                    if sum(vec_mul(x, test_vector)) % 2 != 0 or test_vector == vector:
                        break
                else:
                    orthogonal_vectors.append(test_vector)

            orthogonal_vectors = orthogonal_vectors[1:]
            # проверка на ортогональность

            for options_mul in range(1 << len(orthogonal_vectors)):
                orthogonal_vec_num: int = 0

                val_vector_mul = [1 for x in information]  # заглушка состоящая из одних единиц, нужна для умножения
                for option in IntToBitList(options_mul, size=len(orthogonal_vectors)):
                    if option:
                        val_vector_mul = vec_mul(val_vector_mul, orthogonal_vectors[orthogonal_vec_num])
                    else:
                        val_vector_mul = vec_mul(val_vector_mul, vec_inv(orthogonal_vectors[orthogonal_vec_num]))
                    orthogonal_vec_num += 1

                voice += 1 if sum(vec_mul(val_vector_mul, information)) % 2 != 0 else -1

            result_voice.append(0 if voice < 1 else 1)



"""
        for x in range(len(self.matrix_G) - 1, 0, -1):
            voice: int = 0
            for options_mul in range(1 << len(self.vectors_rise[x - 1])):
                val_vector_mul = [1 for x in information] # заглушка состоящая из одних единиц, нужна для умножения
                counter = 0
                for now_option in IntToBitList(options_mul, size=len(self.vectors_rise[x - 1])):
                    val_vector_mul = vec_mul(val_vector_mul, self.vectors[self.vectors_rise[x - 1][counter]])
                    counter += 1
                print(val_vector_mul)
            pass
"""
