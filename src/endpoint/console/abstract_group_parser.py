# coding=utf-8
import argparse
from abc import ABCMeta
from typing import Optional


class AbstractGroupParser(metaclass=ABCMeta):
    _argument_parser = argparse.ArgumentParser()
    _arguments: None
    _argument_group: None

    @property
    def arguments(self):
        return self._arguments

    @property
    def argument_parser(self) -> argparse.ArgumentParser:
        return self._argument_parser

    def __init__(
            self,
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None
    ):
        if argument_parser:
            self._argument_parser = argument_parser
        else:
            self._argument_parser = argparse.ArgumentParser()

        if argument_group is not None:
            self._argument_group = argument_group
            self._argument_parser = argument_group

    @arguments.setter
    def arguments(self, value):
        self._arguments = value
