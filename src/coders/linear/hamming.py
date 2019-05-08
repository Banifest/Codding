# coding=utf-8
import argparse
from sqlite3 import Connection
from typing import Optional, Union
from uuid import UUID

import math
import numpy as np

from src.coders import abstract_coder
from src.coders.casts import *
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType
from src.statistics.db.table import hamming_table


class Coder(abstract_coder.AbstractCoder):
    type_of_coder = EnumCodersType.HAMMING
    _name = "Hamming"
    _matrixTransformation: List[Union[int, List]] = []

    def __init__(self, length_information: int):
        log.debug("Create of Hamming coder")

        # sum (2**(n-1)-1) from 1 to n must be >= length_information for correct check
        for x in range(1, length_information):
            if 2 ** x - x - 1 >= length_information:
                self.lengthAdditional = x
                break

        self.lengthInformation = length_information
        self.lengthTotal = self.lengthInformation + self.lengthAdditional
        self._matrixTransformation = []

        for x in range(self.lengthAdditional):
            temp: list = []
            flag = True
            # Количество символов требуемых для зануления вначале
            count = (1 << x) - 1
            for y in range((1 << x) - 1):
                temp.append(0)

            while count < self.lengthTotal:
                for y in range(1 << x):
                    temp.append(1) if flag else temp.append(0)
                    count += 1
                    if count >= self.lengthTotal:
                        break
                flag: bool = not flag
            self._matrixTransformation.append(temp)
        # noinspection PyTypeChecker
        self._matrixTransformation = np.transpose(np.array(self._matrixTransformation))

    def encoding(self, information: list) -> list:
        log.info("Encoding package {0} of Hamming coder".format(information))
        list_encoding_information: list = information
        list_encoding_information.reverse()
        if len(list_encoding_information) < self.lengthInformation:
            for x in range(self.lengthInformation - len(list_encoding_information)):
                list_encoding_information.append(0)
        list_encoding_information.reverse()
        code: list = []

        step: int = 0
        # Add checks bits
        for count in range(self.lengthTotal):

            # Check that number enter in set of number (2^n), where n is natural number
            if math.log2(count + 1) != int(math.log2(count + 1)) or step >= self.lengthAdditional:
                code.append([list_encoding_information[count - int(math.log2(count)) - 1]])
            else:
                code.append([0])
                step += 1

        answer = [x[0] for x in code]
        code = np.transpose(np.array(code))
        backup_info = list((np.dot(code, self._matrixTransformation) % 2)[0])
        for x in range(self.lengthAdditional):
            answer[(1 << x) - 1] = backup_info[x]
        return answer

    def decoding(self, information: list) -> list:
        log.info("Decoding package {0} of Hamming coder".format(information))

        code = np.transpose(np.array([[x] for x in information]))
        answer: list = []
        status: list = list((np.dot(code, self._matrixTransformation) % 2)[0])
        status.reverse()
        status: int = bit_list_to_int(status)
        if status != 0:
            log.debug("Обнаруженна(ы) ошибка(и)")

            if len(code[0]) > status - 1:
                code[0][status - 1] = (code[0][status - 1] + 1) % 2
                old_status = status
                status = bit_list_to_int(list((np.dot(code, self._matrixTransformation) % 2)[0]))

                if status != 0:
                    log.debug("Не удалось успешно исправить обнаруженные ошибки")
                    # raise CodingException("Не удалось успешно исправить обнаруженные ошибки")
                log.debug("Произошло успешное исправление ошибки в бите под номером {0}".format(old_status))
            else:
                log.debug("Не удалось успешно исправить обнаруженные ошибки")
                # raise CodingException("Не удалось успешно исправить обнаруженные ошибки")
        count: int = 0
        step: int = 0
        for x in code[0]:
            if math.log2(count + 1) != int(math.log2(count + 1)) or step >= self.lengthAdditional:
                answer.append(x)
            else:
                step += 1
            count += 1
        return answer

    def get_speed(self) -> float:
        return float(self.lengthInformation) / float(self.lengthTotal)

    def try_normalization(self, bit_list: list) -> list:
        return super().try_normalization(bit_list)

    def get_redundancy(self) -> float:
        return super().get_redundancy()

    def to_json(self) -> dict:
        # noinspection PyUnresolvedReferences
        return {
            'name': self.name,
            'length information word': self.lengthInformation,
            'length additional bits': self.lengthAdditional,
            'length coding word': self.lengthTotal,
            'matrix of generating': self._matrixTransformation.tolist(),
            'speed': self.get_speed()
        }

    def save_to_database(self, coder_guid: UUID, connection: Connection) -> None:
        connection.execute(hamming_table.insert().values(
            guid=coder_guid,
            matrix=self._matrixTransformation.tolist()
        ))

    class HammingCoderParser(AbstractGroupParser):
        _prefix: str = ""
        __PACKAGE_LENGTH: str = "hamming_package_length"

        @property
        def hamming_package_length(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__PACKAGE_LENGTH)]

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
                "-{0}hmgpl".format(prefix), "--{0}{1}".format(prefix, self.__PACKAGE_LENGTH),
                type=int,
                help="""Length of package for Hamming coder"""
            )

            # We should parse arguments only for unique coder
            if self._argument_group is None:
                self.arguments = vars(self._argument_parser.parse_args())

    @staticmethod
    def get_coder_parameters(
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None,
            prefix: str = ""
    ) -> HammingCoderParser:
        return Coder.HammingCoderParser(
            argument_parser=argument_parser,
            argument_group=argument_group,
            prefix=prefix
        )
