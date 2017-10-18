import unittest

from coders.hemming import Coder as HemmingCoder


class TestHemmingCoder(unittest.TestCase):  # TODO.txt написать тесты для кодера и декодера хэмминга
    first_coder: HemmingCoder.Coder
    second_coder: HemmingCoder.Coder
    third_coder: HemmingCoder.Coder

    def test_init(self):
        self.first_coder = HemmingCoder.Coder(4)
        self.assertFalse(self.first_coder.lengthTotal == 7)
        self.assertFalse(self.first_coder.lengthInformation == 4)
        self.assertFalse(self.first_coder.lengthAdditional == 3)

        self.second_coder = HemmingCoder.Coder(8)
        self.assertFalse(self.second_coder.lengthTotal == 7)
        self.assertFalse(self.second_coder.lengthInformation == 4)
        self.assertFalse(self.second_coder.lengthAdditional == 3)

        self.third_coder = HemmingCoder.Coder(15)
        self.assertFalse(self.third_coder.lengthTotal == 7)
        self.assertFalse(self.third_coder.lengthInformation == 4)
        self.assertFalse(self.third_coder.lengthAdditional == 3)


    def test_coder(self):
        pass

    def test_decoder(self):
        pass
