# coding=utf-8
import argparse
from sqlite3 import Connection
from typing import Optional
from uuid import UUID

import math
import numpy as np
from numpy.polynomial import polynomial as plm

from src.coders import abstract_coder
from src.coders.casts import int_to_bit_list
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType
from src.statistics.db.table import cyclic_table


class Coder(abstract_coder.AbstractCoder):
    _name = "Циклический"
    polynomial: plm.Polynomial
    type_of_coder = EnumCodersType.CYCLICAL
    matrix_G: np.matrix  # порождающая матрица
    matrix_H: np.matrix  # проверочная матрицал

    def __init__(self, information_length: int, polynomial: int):
        log.debug("Create cyclical coder")

        self.lengthInformation = information_length
        self.lengthAdditional = int(math.log2(polynomial))
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        self.polynomial = plm.Polynomial(int_to_bit_list(polynomial, rev=True))

    def encoding(self, information: list):
        mod: plm.Polynomial = plm.Polynomial([0] * self.lengthAdditional + information) % self.polynomial
        return [int(x) % 2 for x in mod] + [0] * (self.lengthAdditional - len(mod)) + information

    def decoding(self, information: list):
        syndrome: plm.Polynomial = plm.Polynomial(information) % self.polynomial
        for x in range(len(self.polynomial)):
            if sum([int(x) % 2 for x in syndrome]) != 0:
                arr_error: list = [int(x) % 2 for x in syndrome]
                for iter in range(len(arr_error)):
                    if arr_error[iter] != 0:
                        information[iter] ^= 1
            else:
                break

        return information[self.lengthAdditional:]

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    def get_speed(self) -> float:
        return super().get_speed()

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    def to_json(self) -> dict:
        return {'name': self.name,
                'length information word': self.lengthInformation,
                'length additional bits': self.lengthAdditional,
                'length coding word': self.lengthTotal,
                'polynomial': [int(x) for x in self.polynomial],
                'speed': self.get_speed()}

    def save_to_database(self, coder_guid: UUID, connection: Connection) -> None:
        connection.execute(cyclic_table.insert().values(
            guid=coder_guid,
            polynomial=[int(iterator) for iterator in list(self.polynomial)],
        ))

    class CyclicalCoderParser(AbstractGroupParser):
        _prefix: str = ""
        __PACKAGE_LENGTH: str = "cyclic_package_length"
        __POLYNOMIAL: str = "cyclic_polynomial"

        def __init__(
                self,
                argument_parser: Optional[argparse.ArgumentParser] = None,
                argument_group=None,
                prefix: str = ""
        ):
            super().__init__(
                argument_parser=argument_parser,
                argument_group=argument_group
            )
            self._prefix = prefix

            self._argument_parser.add_argument(
                "-{0}cclpl".format(prefix), "--{0}{1}".format(prefix, self.__PACKAGE_LENGTH),
                type=int,
                help="""Length of package for Cyclical coder"""
            )

            self._argument_parser.add_argument(
                "-{0}cclp".format(prefix), "--{0}{1}".format(prefix, self.__POLYNOMIAL),
                type=int,
                help="""Polynomial for Cyclical coder"""
            )

            # We should parse arguments only for unique coder
            if self._argument_group is None:
                self.arguments = vars(self._argument_parser.parse_args())

        @property
        def cyclic_package_length(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__PACKAGE_LENGTH)]

        @property
        def cyclic_polynomial(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__POLYNOMIAL)]

    @staticmethod
    def get_coder_parameters(
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None,
            prefix: str = ""
    ):
        return Coder.CyclicalCoderParser(
            argument_parser=argument_parser,
            argument_group=argument_group,
            prefix=prefix
        )
