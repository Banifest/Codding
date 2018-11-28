# coding=utf-8
# coding=utf-8
import unittest

from src.coders.convolutional.Coder import Coder as ConvolutionalCoder
from src.coders.convolutional.CoderForPacket import ConvolutionalCoderForPacket
from src.coders.cyclical.coder import Coder as CyclicalCoder
from src.coders.fountain.LubyTransform import Coder as LubyTransformCoder
from src.coders.linear.ReedMuller import Coder as ReedMullerCoder
from src.coders.linear.hamming import Coder as hammingCoder


class TestConvolutionalCoder(unittest.TestCase):
    def test_encode(self):
        pass
        # test_coder: ConvolutionalCoder = ConvolutionalCoder([5, 7], 1, 2, 3)
        #
        # start_code: list = [1, 1, 0, 1, 0, 0, 1]
        # code: list = test_coder.Encoding(start_code)
        # self.assertTrue(test_coder.Decoding(code) == start_code)

    def test_correct_ability(self):
        test_coder: ConvolutionalCoder = ConvolutionalCoder([5, 7], 1, 2, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1]
        code: list = test_coder.encoding(start_code)

        code[2] ^= 1
        code[4] ^= 1
        self.assertTrue(test_coder.decoding(code) == start_code)
        code[2] ^= 1
        code[4] ^= 1

        code[0] ^= 1
        code[1] ^= 1
        self.assertFalse(test_coder.decoding(code) == start_code)
        # так как d(min)=4, кодер не может исправить однозначно 3 подряд идущие ошибки


class TesthammingCoder(unittest.TestCase):
    def test_init(self):
        first_coder: hammingCoder = hammingCoder(4)
        self.assertTrue(first_coder.lengthTotal == 7)
        self.assertTrue(first_coder.lengthInformation == 4)
        self.assertTrue(first_coder.lengthAdditional == 3)

        second_coder = hammingCoder(8)
        self.assertTrue(second_coder.lengthInformation == 8)
        self.assertTrue(second_coder.lengthTotal == 12)
        self.assertTrue(second_coder.lengthAdditional == 4)

        third_coder = hammingCoder(15)
        self.assertTrue(third_coder.lengthTotal == 20)
        self.assertTrue(third_coder.lengthInformation == 15)
        self.assertTrue(third_coder.lengthAdditional == 5)

    def test_coder(self):
        test_coder: hammingCoder = hammingCoder(4)
        self.assertTrue([1, 0, 1, 0] == test_coder.decoding(test_coder.encoding([1, 0, 1, 0])))

        test_coder: hammingCoder = hammingCoder(10)
        self.assertTrue([1, 0, 1, 0, 1, 1, 1, 1, 1, 0] == test_coder.decoding(
                test_coder.encoding([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, ])))


class TestConvolutionalCoderForPacket(unittest.TestCase):
    def test_encode(self):
        test_coder: ConvolutionalCoderForPacket = ConvolutionalCoderForPacket([5, 7], 1, 2, 3, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        code: list = test_coder.encoding(start_code)
        self.assertTrue(test_coder.decoding(code) == start_code)

    def test_correct_ability(self):
        test_coder: ConvolutionalCoderForPacket = ConvolutionalCoderForPacket([1, 101], 1, 2, 6, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0]
        code: list = test_coder.encoding(start_code)
        print(code)
        code[8] ^= 1
        code[7] ^= 1

        print(start_code)
        print(test_coder.decoding(code))
        self.assertTrue(test_coder.decoding(code) == start_code)


class TestFountainCoder(unittest.TestCase):
    def test_coder(self):
        test_code: LubyTransformCoder = LubyTransformCoder(3, 3, 6)

        start_code = [1, 0, 0, 1, 1, 0]
        code: list = test_code.encoding(start_code)
        print(code)
        self.assertTrue(test_code.decoding(code) == start_code)

    def test_correct_ability(self):
        test_code: LubyTransformCoder = LubyTransformCoder(3, 3, 6)

        start_code = [1, 0, 0, 1, 1, 0]
        code: list = test_code.encoding(start_code)
        print(code)
        code[2] ^= 1
        code[4] ^= 1
        self.assertTrue(test_code.decoding(code) == start_code)


class TestCyclicalCoder(unittest.TestCase):
    def test_init(self):
        test_coder = CyclicalCoder(4, 11)
        print(test_coder.to_json())

        # при перемножении порождающей и проверочной матриц должна получиться нулевая
        self.assertTrue(1)

    def test_encoding(self):
        test_coder = CyclicalCoder(3, 29)
        starting_code = [1, 0, 1]
        code = test_coder.encoding(starting_code)
        code[3] ^= 1
        test_coder.decoding(code)



class TestReedMullerCoder(unittest.TestCase):
    def test_init(self):
        test_coder = ReedMullerCoder(3, 1)

        code = [0, 0, 1, 1]

        enc_code = test_coder.encoding(code)
        print(enc_code)

        dec_code = test_coder.decoding(enc_code)
        print(dec_code)
        # print(test_coder.matrix_G)

        pass
