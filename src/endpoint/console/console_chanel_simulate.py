# coding=utf-8
from src.endpoint.console.console_coder_simulate import ConsoleCoderSimulate
from src.endpoint.general_chanel_simulate import GeneralChanelSimulate


class ConsoleChanelSimulate(GeneralChanelSimulate):
    """
        Class provide functionality for control testing process
    """
    _firstCoderParams: ConsoleCoderSimulate
    _secondCoderParams: ConsoleCoderSimulate
