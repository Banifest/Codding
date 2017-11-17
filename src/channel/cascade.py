from typing import Optional

from coders.interleaver import Interleaver
from src.channel import channel
from src.coders import abstractCoder
from src.coders.casts import BitListToInt


class Cascade(channel.Channel):
    firstCoder: abstractCoder.AbstractCoder
    firstInterleaver: Interleaver.Interleaver
    secondCoder: abstractCoder.AbstractCoder
    secondInterleaver: Interleaver.Interleaver = None

    def __init__(self,
                 firstCoder: abstractCoder.AbstractCoder,
                 secondCoder: abstractCoder.AbstractCoder,
                 noiseProbability: int or float,
                 countCyclical: Optional[int],
                 duplex: Optional[bool],
                 firstInterleaver: Optional[Interleaver.Interleaver],
                 secondInterleaver: Interleaver.Interleaver or None):
        super().__init__(None, noiseProbability, countCyclical, duplex, firstInterleaver)
        self.firstCoder = firstCoder
        self.secondCoder = secondCoder

        self.secondInterleaver = secondInterleaver if secondInterleaver is not None else None

    def transfer_one_step(self, information: list) -> int:
        self.coder = self.secondCoder
        normalization_information = self.coder.try_normalization(information)

        now_information: list = self.firstCoder.Encoding(normalization_information)

        if self.secondInterleaver is not None:
            now_information = self.secondInterleaver.Shuffle(now_information)

        status: list = self.get_transfer_one_step(now_information)
        now_information = status[0]

        if self.secondInterleaver is not None:
            now_information = self.secondInterleaver.Reestablish(now_information)

        now_information = self.firstCoder.Decoding(now_information)

        return 0 if BitListToInt(now_information) == BitListToInt(information) else 2
