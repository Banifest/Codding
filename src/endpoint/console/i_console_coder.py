# coding=utf-8
import argparse
from abc import abstractmethod, ABC
from typing import Optional


class IConsoleCoder(ABC):

    @staticmethod
    @abstractmethod
    def get_coder_parameters(
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None,
            prefix: str = ""
    ):
        """
        Get Abstract interfaces for getting parameter _coder
        """
        raise NotImplemented
