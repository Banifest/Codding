# coding=utf-8
from typing import Optional

from src.GUI.controller.single_coder_test_thread import SingleCoderTestThread
from src.channel.cascadecodec import CascadeCodec
from src.channel.enum_noise_mode import EnumNoiseMode
from src.coders.abstract_coder import AbstractCoder
from src.coders.interleaver.Interleaver import Interleaver


class CascadeCoderTestThread(SingleCoderTestThread):
    def __init__(
            self,
            noise_chance: float,
            count_test: float,
            test_information: int,
            current_coder: AbstractCoder,
            first_coder: AbstractCoder,
            second_coder: AbstractCoder,
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            is_split_package: bool,
            length_first_interleaver: Optional[int],
            length_second_interleaver: Optional[int],
            last_result: str,
            start: float = 0,
            finish: float = 20,
    ):
        super().__init__(
            noise_chance=noise_chance,
            count_test=count_test,
            test_information=test_information,
            current_coder=current_coder,
            last_result=last_result,
            start=start,
            finish=finish,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
            noise_mode=noise_mode,
            first_interleaver_length=length_first_interleaver
        )

        self.coderSpeed = first_coder.get_speed() * second_coder.get_speed()
        self.coderName = 'Каскадный кодер из: {0} и {1}'.format(first_coder.name, second_coder.name)
        self.channel = CascadeCodec(
            first_coder=first_coder,
            second_coder=second_coder,
            noise_probability=self._noiseChance,
            count_cyclical=self._countTest,
            duplex=False,
            first_interleaver=Interleaver(length_first_interleaver) if length_first_interleaver is not None else None,
            second_interleaver=Interleaver(
                length_second_interleaver) if length_second_interleaver is not None else None,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
            noise_mode=noise_mode,
        )

    def run(self):
        super().run()
