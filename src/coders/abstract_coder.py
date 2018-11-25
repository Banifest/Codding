# coding=utf-8
# coding=utf-8
from abc import ABCMeta, abstractmethod

from src.coders.exeption import CodingException
from src.statistics.db.coderentity import CoderEntity


class AbstractCoder:
    __metaclass__ = ABCMeta
    name: str = ""
    type_of_coder: CoderEntity.CodersType
    coding_information: int = 0
    countAdditional: int = 0
    lengthTotal: int = 0
    lengthInformation: int = 0
    is_div_into_package = True

    @abstractmethod
    def encoding(self, information: int or list) -> list:
        """
        Args:
            information: list of bits for encoding
        Returns:
            list: encoding list of bits
        """
        pass

    @abstractmethod
    def decoding(self, information: list) -> list:
        """
        Args:
            information: list of bits for decoding
        Returns:
            list: decoding list of bits
        """
        pass

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
            raise CodingException("Невозможно привести информационное слово с большей длиной к меньшему")
        else:
            return (self.lengthInformation - len(bit_list)) * [0] + bit_list

    @abstractmethod
    def to_json(self) -> dict:
        return {}
