import unittest

from coders.convolutional.Coder import Coder as ConvolutionalCoder
from coders.hemming.Coder import Coder as HemmingCoder


class TestConvolutionalCoder(unittest.TestCase):
    def test_encode(self):
        test_coder: ConvolutionalCoder = ConvolutionalCoder([5, 7], 1, 2, 3)
        code: list = test_coder.Encoding([1, 1, 0, 1])
        self.assertTrue(test_coder.Decoding(code) == [1, 1, 0, 1])


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
    pass
