# coding=utf-8
from GUI.controller.single_coder_test_thread import SingleCoderTestThread
from channel.enum_noise_mode import EnumNoiseMode
from src.channel.cascadecodec import CascadeCodec
from src.coders.abstract_coder import AbstractCoder
from statistics.object.test_result_serializer import TestResultSerializer


class CascadeCoderTestThread(SingleCoderTestThread):
    def __init__(self,
                 noise_chance: float,
                 count_test: float,
                 test_info: int,
                 current_coder: AbstractCoder,
                 first_coder: AbstractCoder,
                 second_coder: AbstractCoder,
                 noise_mode: EnumNoiseMode,
                 noise_package_length: int,
                 is_split_package: bool,
                 last_result: str,
                 start: float = 0,
                 finish: float = 20,
                 mode: int = 0
                 ):
        super().__init__(
            noise_chance=noise_chance,
            count_test=count_test,
            test_info=test_info,
            current_coder=current_coder,
            last_result=last_result,
            start=start,
            finish=finish,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
            noise_mode=noise_mode,
        )

        self.coderSpeed = first_coder.get_speed() * second_coder.get_speed()
        self.coderName = 'Каскадный кодер из: {0} и {1}'.format(first_coder.name, second_coder.name)
        self.channel = CascadeCodec(
            first_coder=first_coder,
            second_coder=second_coder,
            noise_probability=self.noiseChance,
            count_cyclical=self.countTest,
            duplex=False,
            first_interleaver=None,
            second_interleaver=None,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
            noise_mode=noise_mode,
        )

    def run(self):
        self.information_dict['is_cascade'] = True
        self.information_dict['coder'] = {
            'first_coder': self.channel.firstCoder.to_json(),
            'second_coder': self.channel.secondCoder.to_json(),
            'name': self.coderName,
            'speed': self.coderSpeed
        }
        super().run()
        if self.information_dict['is_cascade']:
            TestResultSerializer().serialize_to_db(
                self.information_dict,
                self.channel.firstCoder,
                self.channel.secondCoder
            )
