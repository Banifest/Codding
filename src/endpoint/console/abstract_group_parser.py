# coding=utf-8
import argparse
from abc import ABC
from typing import Optional


class AbstractGroupParser(ABC):
    _argumentParser = argparse.ArgumentParser()
    _arguments: Optional[None]
    _argumentGroup: Optional[None]

    @property
    def arguments(self):
        return self._arguments

    @property
    def argument_parser(self) -> argparse.ArgumentParser:
        return self._argumentParser

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None
    ):
        if argument_parser:
            self._argumentParser = argument_parser
        else:
            self._argumentParser = argparse.ArgumentParser()

        if argument_group is not None:
            self._argumentGroup = argument_group
            self._argumentParser = argument_group

    @arguments.setter
    def arguments(self, value):
        self._arguments = value
