import random


def GenInterference(information: list, straight: int) -> list:
    randomGenerator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел
    answer: list = []
    for x in information:
        if randomGenerator.randint(0, 100) < straight:
            answer.append(x * randomGenerator.getrandbits(1))
        else:
            answer.append(x)
    return answer
