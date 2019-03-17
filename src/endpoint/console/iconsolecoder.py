# coding=utf-8
from abc import ABCMeta, abstractmethod


class IConsoleCoder(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def get_coder_parameters():
        raise NotImplemented
