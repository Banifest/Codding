from math import log2

from src.coders.convolutional.Coder import Coder


class ConvolutionalCoderForPacket(Coder):
    name = "Сверточный для пакетов"

    def __init__(self, list_polynomials: list, count_input: int, count_output: int,
                 count_register: int, count_control_bits: int):
        new_list_polynomials = []
        for polynomial in list_polynomials:
            new_polynomial: int = polynomial & 1

            for degree in range(1, int(log2(polynomial)) + 1):
                if (1 << degree) & polynomial:
                    new_polynomial += (1 << (degree * count_control_bits))

            new_list_polynomials.append(new_polynomial)

        print(new_list_polynomials)
        super().__init__(new_list_polynomials, count_input, count_output, count_register)
