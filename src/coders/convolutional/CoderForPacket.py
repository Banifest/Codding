from coders.casts import BitListToInt, IntToBitList
from coders.convolutional.Coder import Coder


class ConvolutionalCoderForPacket(Coder):
    def __init__(self, list_polynomials: list, count_input: int, count_output: int,
                 count_register: int, count_control_bits: int):
        list_polynomials = IntToBitList(BitListToInt(list_polynomials) << count_control_bits)

        super().__init__(list_polynomials, count_input, count_output, count_register)
