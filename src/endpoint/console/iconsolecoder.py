from abc import ABCMeta, abstractmethod


class IConsoleCoder(metaclass=ABCMeta):

    @abstractmethod
    def get_coder_parameters(self):
        pass
