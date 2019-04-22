# coding=utf-8


def int_to_bit_list(num: int, size: int = None, rev: bool = False) -> list:
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


def bit_list_to_int_list(num: list) -> list:
    it: int = 0
    answer: list = []

    num.reverse()
    for x in num:
        if x != 0:
            answer.append(it)
        it += 1
    return answer


def bit_list_to_int(num: list, rev: bool = False) -> int:
    """

    :param num:
    :param rev:
    :return:
    """
    if rev:
        num.reverse()

    it = 1 << len(num) - 1
    answer = 0
    for x in num:
        answer += it * x
        it >>= 1
    return answer


def bit_list_comb_to_int(num: list) -> int:
    """

    :param num:
    :return:
    """
    answer: int = 0
    for x in num:
        answer += 1 << x
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


def get_hamming_distance(first: list, second: list) -> int:
    """

    :param first:
    :param second:
    :return:
    """
    answer: int = 0
    if len(first) != len(second):
        raise Exception("Списки должны быть одинаковой длины")

    for x in range(len(first)):
        if first[x] != second[x]:
            answer += 1
    return answer


def str_list_to_list(value: str) -> list:
    """
    :param value:
    :return:
    """
    return [int(x) for x in value.split(",")]
