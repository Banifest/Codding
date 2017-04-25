import random


def GenInterference(info: list, straight: float) -> list:
    answer = []
    for x in info:
        if random.random() <= straight:
            answer.append(x * int(random.random() + 0.5))
        else:
            answer.append(x)
    return answer


def GetRandomBool():
    return bool(random.randrange(0, 2))
