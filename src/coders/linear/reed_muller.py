# coding=utf-8
import itertools
import uuid

import numpy as np
from sqlalchemy.engine import Connection

from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int, int_to_bit_list


class Coder(abstract_coder.AbstractCoder):
    def save_to_database(self, coder_guid: uuid.UUID, connection: Connection):
        raise NotImplemented

    def get_coder_parameters(self):
        raise NotImplemented

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    def get_speed(self) -> float:
        return super().get_speed()

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    _name = "Рида-Миллера"

    matrix_G: np.matrix
    vectors: list
    vectors_rise: list = []
    r: int
    power: int

    def __init__(self, power: int, r: int):
        self.r = r
        self.power = power

        init_matrix: list = [int_to_bit_list((2 ** (2 ** self.power)) - 1)]
        if r > 0:
            self.vectors = np.matrix(
                [int_to_bit_list(x, size=self.power) for x in range(2 ** self.power)]).T.tolist()
            init_matrix += self.vectors
            matrix_int_g1 = [bit_list_to_int(x) for x in init_matrix[1:]]
            self.vectors_rise = [[x] for x in range(1, self.power + 1)]

        for x in range(r - 1):
            comb: list = list(itertools.combinations(range(self.power), x + 2))

            new_matrix_g: list = []
            self.vectors_rise += comb
            for x in comb:
                val: int = matrix_int_g1[x[0]]
                for y in x:
                    val &= matrix_int_g1[y]
                new_matrix_g.append(int_to_bit_list(val, size=1 << self.power))
            init_matrix += new_matrix_g

        self.matrix_G = np.matrix(init_matrix)
        self.lengthInformation = len(self.matrix_G.tolist())
        self.lengthTotal = len(self.matrix_G.tolist()[0])
        self.lengthAdditional = self.lengthTotal - self.lengthInformation

    def encoding(self, information: list):
        information[0] = 0
        return [x % 2 for x in (np.matrix(information) * self.matrix_G).tolist()[0]]

    def decoding(self, information: list):
        def vec_xor(a, b):
            return [a[i] ^ b[i] for i in range(len(a))]

        def vec_mul(a, b):
            return [a[i] & b[i] for i in range(len(a))]

        def vec_inv(a):
            return [x ^ 1 for x in a]

        def vec_gen(a, b):
            return [a for x in range(b)]

        result_voice: list = []
        for vector in self.matrix_G.tolist()[::-1][:-1]:
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

                val_vector_mul = vec_gen(1, len(information))  # заглушка состоящая из одних единиц, нужна для умножения
                for option in int_to_bit_list(options_mul, size=len(orthogonal_vectors)):
                    if option:
                        val_vector_mul = vec_mul(val_vector_mul, orthogonal_vectors[orthogonal_vec_num])
                    else:
                        val_vector_mul = vec_mul(val_vector_mul, vec_inv(orthogonal_vectors[orthogonal_vec_num]))
                    orthogonal_vec_num += 1

                voice += 1 if sum(vec_mul(val_vector_mul, information)) % 2 != 0 else -1

            result_voice.append(0 if voice < 1 else 1)

        first_sum: int = information.copy()
        counter: int = 0
        for vector in self.matrix_G.tolist()[::-1][:-1]:
            first_sum = vec_xor(vec_mul(vector, vec_gen(result_voice[counter], len(information))), first_sum)
            counter += 1

        result_voice.append(0 if sum(first_sum) > 5 else 1)
        temp_matrix: list = self.matrix_G.tolist()
        result_voice.reverse()
        decoding_information: list = vec_gen(0, len(information))
        for x in range(len(temp_matrix)):
            decoding_information = vec_xor(vec_mul(temp_matrix[x], vec_gen(result_voice[x], len(information))),
                                           decoding_information)

        decoding_information.reverse()  # исправленное кодовое слово
        result_voice[0] = 0 if sum(decoding_information) < 5 else 1

        return result_voice

    def to_json(self) -> dict:
        return {'name': self.name,
                'length _information word': self.lengthInformation,
                'length additional bits': self.lengthAdditional,
                'length coding word': self.lengthTotal,
                'matrix of generating': self.matrix_G.tolist(),
                'speed': self.get_speed()}
