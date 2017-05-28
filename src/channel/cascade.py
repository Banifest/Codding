from typing import Optional

from src.channel import channel
from src.coders import abstractCoder
from src.coders.interleaver import Interleaver


class Cascade(channel.Channel):
    firstCoder: abstractCoder.Coder
    firstInterleaver: Interleaver.Interleaver
    secondCoder: abstractCoder.Coder
    secondInterleaver: Interleaver.Interleaver

    def __init__(self, firstCoder: abstractCoder.Coder, secondCoder: abstractCoder.Coder,
                 noiseProbability: Optional[int], countCyclical: Optional[int],
                 duplex: Optional[bool], firstInterleaver: Optional[Interleaver.Interleaver],
                 secondInterleaver: Optional[Interleaver.Interleaver]):
        super().__init__(None, noiseProbability, countCyclical, duplex, firstInterleaver)
        self.firstCoder = firstCoder
        self.secondCoder = secondCoder
        if secondInterleaver is not None: self.secondInterleaver = secondInterleaver


    def TransferOneStep(self, information: list) -> int:
        self.coder = self.secondCoder
        nowInformation: list = self.firstCoder.Encoding(information)

        if self.secondInterleaver is not None: nowInformation = self.secondInterleaver.Shuffle(nowInformation)
        status: list = self.GetTransferOneStep(nowInformation)
        nowInformation = status[0]
        if self.secondInterleaver is not None: nowInformation = self.secondInterleaver.Reestablish(nowInformation)

        nowInformation = self.firstCoder.Decoding(nowInformation)

        return 0 if nowInformation == information else 2
