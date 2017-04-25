from random import random


def GenInterference(info: list, straight: float) -> list:  # TODO.txt исправить на корректную генерацию помех
    answer = []
    for x in info:
        if random() >= straight:
            answer.append(x * int(random() + 0.5))
        else:
            answer.append(x)
    return answer


def GetRandomBool():
    return bool(random.randrange(0, 2))
