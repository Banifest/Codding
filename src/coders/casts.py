# coding=utf-8
from typing import List

from src.helper.error.exception.codding_exception import CodingException


def int_to_bit_list(num: int, size: int = None, rev: bool = False) -> List[int]:
    """
    Convert numeric integer to bits list
    Example: num: int = 100; size = None; return [1, 1, 0, 0, 1, 0, 0]
    :param num: int
    :param size: int. If length of output list less then size, then add [0] * ( size - len(list)) to list
    :param rev: bool
    :return: list
    """
    iterator: int = 1
    answer: list = []
    while iterator <= num:
        if num | iterator == num:
            answer.append(1)
        else:
            answer.append(0)
        iterator <<= 1
    if size is not None:
        answer += [0] * (size - len(answer))
    if not rev:
        answer.reverse()
    return answer


def bit_list_to_int_list(num: list) -> List[int]:
    it: int = 0
    answer: list = []

    num.reverse()
    for x in num:
        if x != 0:
            answer.append(it)
        it += 1
    return answer


def bit_list_to_int(num: List[int], rev: bool = False) -> int:
    """
    Convert list of bits to integer
    :param num: List[int]
    :param rev: bool Default value = False
    :return: int
    """
    if rev:
        num.reverse()

    it = 1 << len(num) - 1
    answer = 0
    for power in num:
        answer += it * power
        it >>= 1
    return answer


def cycle_shift_list(num: list, right: bool = True, count: int = 1):
    """

    :param num:
    :param right:
    :param count:
    :return:
    """
    if right:
        return num[-count:] + num[:-count]
    else:
        return num[count:] + num[:count]


def get_hamming_distance(first: List[int], second: List[int]) -> int:
    """
    Determined Hamming distance
    :param first: List[int]
    :param second: List[int]
    :return: hamming's distance between first and second
    """
    distance: int = 0
    if len(first) != len(second):
        raise CodingException(
            message="Cannot determine hamming's distance between list with different length"
        )

    for iterator in range(len(first)):
        if first[iterator] != second[iterator]:
            distance += 1
    return distance


def str_list_to_list(value: str) -> list:
    """
    :param value:
    :return:
    """
    return [int(x) for x in value.split(",")]
