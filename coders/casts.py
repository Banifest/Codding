def IntToBitList(num: int)->list:
    it = 1
    answer = []
    while it <= num:
        if num | it == num:
            answer.append(1)
        else:
            answer.append(0)
        it <<= 1
    return answer


def BitListToInt(num: list)->int:
    it = 1 << len(num) - 1
    answer = 0
    for x in num:
        answer += it * x
        it >>= 1
    return answer

def BitListCombToInt(num: list)->int:
    answer = 0
    for x in num:
        answer += 1 << x
    return answer