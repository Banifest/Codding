# coding=utf-8
from abc import ABCMeta, abstractmethod
from collections import defaultdict

from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.endpoint.console.iconsolecoder import IConsoleCoder
from src.helper.error.exception.codding_exception import CodingException
from src.statistics.db.enum_coders_type import EnumCodersType
from src.statistics.object.idatabaseserialize import IDataBaseSerialize


class __ObserverMeta(ABCMeta):
    inheritors_classes = defaultdict(list)

    def __new__(mcs, name, bases, dct):
        inherit_class = type.__new__(mcs, name, bases, dct)
        for base in inherit_class.mro()[1:-1]:
            mcs.inheritors_classes[base].append(inherit_class)
        return inherit_class


class AbstractCoder(IConsoleCoder, IDataBaseSerialize, metaclass=__ObserverMeta):
    type_of_coder: EnumCodersType
    _name: str = ""
    coding_information: int = 0
    countAdditional: int = 0
    lengthTotal: int = 0
    lengthInformation: int = 0
    is_div_into_package = True

    @staticmethod
    def get_inheritors_coder_classes() -> list:
        return __class__.inheritors_classes[__class__]

    @property
    def name(self):
        return self._name

    @abstractmethod
    def encoding(self, information: int or list) -> list:
        """
        Args:
            information: list of bits for encoding
        Returns:
            list: encoding list of bits
        """
        raise NotImplementedError

    @abstractmethod
    def decoding(self, information: list) -> list:
        """
        Args:
            information: list of bits for decoding
        Returns:
            list: decoding list of bits
        """
        raise NotImplementedError

    @abstractmethod
    def get_redundancy(self) -> float:
        """
        Method for get redundancy information
        Returns:
            redundancy information for this coder
        """
        return self.countAdditional / self.lengthInformation

    @abstractmethod
    def get_speed(self) -> float:
        """
        Method for get coderSpeed coder
        Returns:
            float coderSpeed coder
        """
        return self.lengthInformation / self.lengthTotal

    @abstractmethod
    def try_normalization(self, bit_list: list) -> list:
        """
        Method for try normalization input information for successful encoding
        if normalization is possible return: bit_list else raise CodingException
        Args:
            bit_list: list consist of 0 or 1

        Returns: list consist of 0 or 1

        """
        if len(bit_list) > self.lengthInformation:
            raise CodingException(
                message=CodingException.LENGTH_OF_INPUT_PACKAGE_OVERFLOW.message,
                long_message=CodingException.LENGTH_OF_INPUT_PACKAGE_OVERFLOW.long_message,
                additional_information=[self.name, self.lengthInformation, len(bit_list)]
            )
        else:
            return (self.lengthInformation - len(bit_list)) * [0] + bit_list

    @abstractmethod
    def to_json(self) -> dict:
        return {}

    @staticmethod
    @abstractmethod
    def get_coder_parameters() -> AbstractGroupParser:
        """
        Get Abstract interfaces for getting parameter coder
        """
        raise NotImplementedError
