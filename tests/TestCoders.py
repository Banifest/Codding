import unittest

from numpy.polynomial import polynomial as plm

from coders.convolutional.Coder import Coder as ConvolutionalCoder
from coders.convolutional.CoderForPacket import ConvolutionalCoderForPacket
from coders.cyclical.Coder import Coder as CyclicalCoder
from coders.fountain.LubyTransform import Coder as LubyTransformCoder
from coders.hemming.Coder import Coder as HemmingCoder


class TestConvolutionalCoder(unittest.TestCase):
    def test_encode(self):
        test_coder: ConvolutionalCoder = ConvolutionalCoder([5, 7], 1, 2, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1]
        code: list = test_coder.Encoding(start_code)
        self.assertTrue(test_coder.Decoding(code) == start_code)

    def test_correct_ability(self):
        test_coder: ConvolutionalCoder = ConvolutionalCoder([5, 7], 1, 2, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1]
        code: list = test_coder.Encoding(start_code)

        code[2] ^= 1
        code[4] ^= 1
        self.assertTrue(test_coder.Decoding(code) == start_code)
        code[2] ^= 1
        code[4] ^= 1

        code[0] ^= 1
        code[1] ^= 1
        self.assertFalse(test_coder.Decoding(code) == start_code)
        # так как d(min)=4, кодер не может исправить однозначно 3 подряд идущие ошибки


class TestHemmingCoder(unittest.TestCase):
    def test_init(self):
        first_coder: HemmingCoder = HemmingCoder(4)
        self.assertTrue(first_coder.lengthTotal == 7)
        self.assertTrue(first_coder.lengthInformation == 4)
        self.assertTrue(first_coder.lengthAdditional == 3)

        second_coder = HemmingCoder(8)
        self.assertTrue(second_coder.lengthInformation == 8)
        self.assertTrue(second_coder.lengthTotal == 12)
        self.assertTrue(second_coder.lengthAdditional == 4)

        third_coder = HemmingCoder(15)
        self.assertTrue(third_coder.lengthTotal == 20)
        self.assertTrue(third_coder.lengthInformation == 15)
        self.assertTrue(third_coder.lengthAdditional == 5)

    def test_coder(self):
        test_coder: HemmingCoder = HemmingCoder(4)
        self.assertTrue([1, 0, 1, 0] == test_coder.Decoding(test_coder.Encoding([1, 0, 1, 0])))

        test_coder: HemmingCoder = HemmingCoder(12)
        self.assertTrue([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0] == test_coder.Decoding(
                test_coder.Encoding([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0])))


class TestConvolutionalCoderForPacket(unittest.TestCase):
    def test_encode(self):
        test_coder: ConvolutionalCoderForPacket = ConvolutionalCoderForPacket([5, 7], 1, 2, 3, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        code: list = test_coder.Encoding(start_code)
        self.assertTrue(test_coder.Decoding(code) == start_code)

    def test_correct_ability(self):
        test_coder: ConvolutionalCoderForPacket = ConvolutionalCoderForPacket([1, 101], 1, 2, 6, 3)

        start_code: list = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0]
        code: list = test_coder.Encoding(start_code)
        print(code)
        code[8] ^= 1
        code[7] ^= 1

        print(start_code)
        print(test_coder.Decoding(code))
        self.assertTrue(test_coder.Decoding(code) == start_code)


class TestFountainCoder(unittest.TestCase):
    def test_coder(self):
        test_code: LubyTransformCoder = LubyTransformCoder(3, 3, 6)

        start_code = [1, 0, 0, 1, 1, 0]
        code: list = test_code.Encoding(start_code)
        print(code)
        self.assertTrue(test_code.Decoding(code) == start_code)

    def test_correct_ability(self):
        test_code: LubyTransformCoder = LubyTransformCoder(3, 3, 6)

        start_code = [1, 0, 0, 1, 1, 0]
        code: list = test_code.Encoding(start_code)
        print(code)
        code[2] ^= 1
        code[4] ^= 1
        self.assertTrue(test_code.Decoding(code) == start_code)


class TestCyclicalCoder(unittest.TestCase):
    def test_get_remainder(self):
        test_coder = CyclicalCoder(4, 11)

        p1 = plm.Polynomial([1, 1, 0, 1])
        p2 = plm.Polynomial([0, 0, 1])
        a = [1, 2, 3, 4, 5, 6]

        print([int(x) for x in (p2 % p1)])

        pass
