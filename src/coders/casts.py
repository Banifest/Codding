# coding=utf-8


def IntToBitList(num: int, size: int = None, rev: bool = False) -> list:
    it: int = 1
    answer: list = []
    while it <= num:
        if num | it == num:
            answer.append(1)
        else:
            answer.append(0)
        it <<= 1
    if size is not None:
        answer += [0] * (size - len(answer))
    if not rev:
        answer.reverse()
    return answer


def BitListToIntList(num: list) -> list:
    it: int = 0
    answer: list = []

    num.reverse()
    for x in num:
        if x != 0:
            answer.append(it)
        it += 1
    return answer


def BitListToInt(num: list, rev: bool = False) -> int:
    if rev:
        num.reverse()

    it = 1 << len(num) - 1
    answer = 0
    for x in num:
        answer += it * x
        it >>= 1
    return answer


def BitListCombToInt(num: list) -> int:
    answer: int = 0
    for x in num:
        answer += 1 << x
    return answer


def cycle_shift_list(num: list, right: bool = True, count: int = 1):
    if right:
        return num[-count:] + num[:-count]
    else:
        return num[count:] + num[:count]


def GetHemmingDistance(first: list, second: list) -> int:
    answer: int = 0
    if len(first) != len(second):
        raise Exception("Списки должны быть одинаковой длины")

    for x in range(len(first)):
        if first[x] != second[x]:
            answer += 1
    return answer


def StrListToList(value: str) -> list:
    # TODO Нужно будет переписать
    try:
        return [int(x) for x in value.split(",")]
    except:
        pass
