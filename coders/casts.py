import math


def IntToBitList(num: int) -> list:
    it = 1
    answer = []
    while it <= num:
        if num | it == num:
            answer.append(1)
        else:
            answer.append(0)
        it <<= 1
    answer.reverse()
    return answer


def BitListToInt(num: list) -> int:
    it = 1 << len(num) - 1
    answer = 0
    for x in num:
        answer += it * x
        it >>= 1
    return answer


def BitListCombToInt(num: list) -> int:
    answer = 0
    for x in num:
        answer += 1 << x
    return answer


def CycleShiftRightBitList(num: list) -> list:
    num = num.copy()
    return num[-1] + num[:-1]


def CycleShiftLeftBitList(num: list) -> list:
    num = num.copy()
    return num[1:] + num[0]


def CycleShiftRight(num: int) -> int:
    juniorBit = num & 1
    num >>= 1
    return (juniorBit << (math.log2(num) + 1)) + num


def CycleShiftLeft(num: int) -> int:
    olderBit = num & (1 << math.log2(num))
    return (((olderBit - 1) & num) << 1) + 1
