# coding=utf-8
import argparse
from sqlite3 import Connection
from typing import Optional, List
from uuid import UUID

from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int, get_hamming_distance, int_to_bit_list, cycle_shift_list
from src.endpoint.console.abstract_group_parser import AbstractGroupParser
from src.logger import log
from src.statistics.db.enum_coders_type import EnumCodersType
from src.statistics.db.table import convolution_table


class Coder(abstract_coder.AbstractCoder):
    """
    Convolution coder class
    """
    _name = "Сверточный"
    typeOfCoder = EnumCodersType.CONVOLUTION
    __MAX_STEPS: int = 9999999999999

    _countPolynomials: int = 0
    _listPolynomials: List[int] = []
    _countInput: int = 0
    _countOutput: int = 0
    _countRegisters: int = 0
    _register: int = 0
    _graph: List[List[List[int]]] = []
    isDivIntoPackage: bool = False

    def __init__(
            self,
            list_polynomials: list,
            count_input: int,
            count_output: int,
            count_register: int
    ):
        log.debug("Create convolution coder")
        self._countInput = count_input
        self._countOutput = count_output
        self._countRegisters = count_register
        self._countPolynomials = len(list_polynomials)
        self._listPolynomials = list_polynomials

        self.lengthTotal = self._countOutput + self._countInput
        self.lengthInformation = 1
        self.lengthAdditional = self.lengthTotal - self.lengthInformation

        self._graph = self._get_graph()

    def get_speed(self) -> float:
        """
        Method contain functionality for calculation speed of this coder configuration
        :return:
        """
        return 1 / self._countRegisters

    def get_redundancy(self) -> float:
        """
        Method contain functionality for calculation redundancy of this coder configuration
        :return:
        """
        return self._countOutput

    def _do_step(self, information_bit: int) -> list:
        """
        Method contain functionality for generation _graph of
        :param information_bit:
        :return:
        """
        log.debug("Step coding convolution - {0}".format(information_bit))
        self._register <<= 1

        # зануление старшего бита
        self._register &= (1 << (self._countRegisters + 1)) - 1
        self._register += information_bit

        answer = []
        power = 0
        for count in range(self._countPolynomials):
            added_bit = 0
            for x in int_to_bit_list(self._listPolynomials[count] & self._register):
                added_bit ^= x
            answer.append(added_bit % 2)
            power += 1
        return answer

    def _get_graph(self) -> List[List[List[int]]]:
        """
        Формирует список представляющий граф переходов, где каждая вершина
        [
            [номер вершины в которую переходим, [биты которые соответвуют переходу]],
            ...
        ]
        """
        answer: list = []
        for x in range(2 ** self._countRegisters):
            vertex: list = []
            self._register = x
            list_integers: list = int_to_bit_list(x, self._countRegisters)
            list_integers = cycle_shift_list(list_integers)
            list_integers[0] = 0
            vertex.append([bit_list_to_int(list_integers), self._do_step(0)])
            self._register = x
            list_integers[0] = 1
            vertex.append([bit_list_to_int(list_integers), self._do_step(1)])
            answer.append(vertex)

        self._register = 0
        return answer

    def encoding(self, information: list) -> list:
        """
        TODO
        :param information:
        :return:
        """
        log.info("Кодирование пакета {0} свёрточным кодером".format(information))
        answer: list = []

        # текущая вершина
        current_vertex: int = 0
        for nowBit in information:
            answer.append(self._graph[current_vertex][nowBit][1])
            current_vertex = self._graph[current_vertex][nowBit][0]

        answer = [y for x in answer for y in x]
        return answer

    def decoding(self, information: list):
        """
        TODO
        :param information:
        :return:
        """
        log.info("Декодирование пакета {0} свёрточным декодером по максимуму правдоподобия".format(information))
        # last_step: list = []  # Информация об предыдущем шаге
        # now_step: list = []  # Информация о текущем шаге
        # info_about_vertex: list = []  # информация о вершине
        # travel: list = []  # путь для текущей вершины
        # cost_travel: int = 0  # стоимость для текущего пути

        info_divided_into_steps: list = []  # информация поделенная на шаги
        for x in range(0, len(information), self._countOutput):
            count: int = 0
            temp_list: list = []
            while count < self._countOutput:
                temp_list.append(information[x + count])
                count += 1
            info_divided_into_steps.append(temp_list)

        last_step = now_step = [[0, []]] + [[self.__MAX_STEPS, []] for x in
                                            range(2 ** self._countRegisters - 1)]  # заполняет первый шаг

        for x in info_divided_into_steps:
            now_step = [[self.__MAX_STEPS, []] for x in range(2 ** self._countRegisters)]
            number: int = 0
            for info_about_vertex in last_step:
                vertex_step: int = self._graph[number][0][0]  # вершина перехода
                distance: int = get_hamming_distance(x, self._graph[number][0][1])
                if now_step[vertex_step][0] > last_step[number][0] + distance:
                    now_step[vertex_step] = [info_about_vertex[0] + distance, info_about_vertex[1] + [0]]

                vertex_step: int = self._graph[number][1][0]  # вершина перехода
                distance: int = get_hamming_distance(x, self._graph[number][1][1])
                if now_step[vertex_step][0] > last_step[number][0] + distance:
                    now_step[vertex_step] = [info_about_vertex[0] + distance, info_about_vertex[1] + [1]]

                number += 1
            last_step = now_step

        min_answer: list = []
        min_cost: int = self.__MAX_STEPS
        for x in last_step:
            if min_cost > x[0]:
                min_cost = x[0]
                min_answer = x[1]
        return min_answer

    def try_normalization(self, bit_list: List[int]) -> List[int]:
        """
        TODO
        :param bit_list:
        :return:
        """
        return bit_list

    def to_json(self) -> dict:
        """
        TODO
        :return:
        """
        return {
            'name': self._name,
            'count inputs': self._countInput,
            'count polynomials': self._countPolynomials,
            'list of polynomials': self._listPolynomials,
            'count of outputs': self._countOutput,
            'count of registers': self._countRegisters,
            '_graph': self._graph,
            'speed': self.get_speed()
        }

    def save_to_database(self, coder_guid: UUID, connection: Connection) -> None:
        connection.execute(convolution_table.insert().values(
            guid=coder_guid,
            count_polynomial=self._countPolynomials,
            count_input_bits=self._countInput,
            count_output_bits=self._countOutput,
            count_registers=self._countRegisters,
        ))

    class ConvolutionCoderParser(AbstractGroupParser):
        _prefix: str = ""
        __POLYNOMIAL_LIST: str = "convolution_polynomial_list"
        __QUANTITY_MEMORY_REGISTER: str = "convolution_quantity_memory_register"

        # noinspection SpellCheckingInspection
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

            self._argumentParser.add_argument(
                "-{0}cnvlp".format(prefix), "--{0}{1}".format(prefix, self.__POLYNOMIAL_LIST),
                type=str,
                help="""List of polynomial"""
            )

            self._argumentParser.add_argument(
                "-{0}cnvmr".format(prefix), "--{0}{1}".format(prefix, self.__QUANTITY_MEMORY_REGISTER),
                type=int,
                help="""Quantity of memory registers of counvolution coder"""
            )

            # We should parse arguments only for unique coder
            if self._argumentGroup is None:
                self.arguments = vars(self._argumentParser.parse_args())

        @property
        def convolution_polynomial_list(self) -> str:
            return self.arguments["{0}{1}".format(self._prefix, self.__POLYNOMIAL_LIST)]

        @property
        def convolution_memory_register(self) -> int:
            return self.arguments["{0}{1}".format(self._prefix, self.__QUANTITY_MEMORY_REGISTER)]

    @staticmethod
    def get_coder_parameters(
            argument_parser: Optional[argparse.ArgumentParser] = None,
            argument_group=None,
            prefix: str = ""
    ):
        return Coder.ConvolutionCoderParser(
            argument_parser=argument_parser,
            argument_group=argument_group,
            prefix=prefix
        )
