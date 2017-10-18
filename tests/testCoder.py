import unittest

from coders.hemming import Coder as HemmingCoder


class TestHemmingCoder(unittest.TestCase):  # TODO.txt написать тесты для кодера и декодера хэмминга

    def test_init(self):
        first_coder = HemmingCoder.Coder(4)
        self.assertFalse(first_coder.lengthTotal == 7)
        self.assertFalse(first_coder.lengthInformation == 4)
        self.assertFalse(first_coder.lengthAdditional == 3)

        second_coder = HemmingCoder.Coder(8)
        self.assertFalse(second_coder.lengthTotal == 12)
        self.assertFalse(second_coder.lengthInformation == 8)
        self.assertFalse(second_coder.lengthAdditional == 4)

        third_coder = HemmingCoder.Coder(15)
        self.assertFalse(third_coder.lengthTotal == 20)
        self.assertFalse(third_coder.lengthInformation == 4)
        self.assertFalse(third_coder.lengthAdditional == 3)

    def test_coder(self):
        test_coder: HemmingCoder.Coder = HemmingCoder.Coder(4)
        self.assertTrue([1, 0, 1, 0] == test_coder.Decoding(test_coder.Encoding([1, 0, 1, 0])))

        test_coder: HemmingCoder.Coder = HemmingCoder.Coder(12)
        self.assertTrue([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0] == test_coder.Decoding(
            test_coder.Encoding([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0])))
