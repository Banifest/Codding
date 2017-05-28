def GetCombinations(n: int, k: int) -> list:
    answer: list = []
    for x in range(0, 1 << n):
        if GetCountOneBit(x) == k:
            answer.append(GetListOneCombination(x))

    return answer


def GetCountOneBit(num: int) -> int:
    count: int = 0
    while num != 0:
        if num | 1 == num:
            count += 1
        num >>= 1
    return count


def GetListOneCombination(num: int) -> list:
    count: int = 1
    p: int = 0
    answer: list = []
    while count <= num:
        if num | count == num:
            answer.append(p)
        p += 1
        count <<= 1
    return answer