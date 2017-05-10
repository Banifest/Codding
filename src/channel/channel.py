import random
from typing import Optional


class Channel:
    noiseProbability: int = 0


    def GenInterference(self, information: list, straight: Optional[int]) -> list:
        """
        Генерация помех с задданной вероятностью
        :param information: list Информация, представленная в виде массива битов:
        :param straight: Optional[int] Вероятность помех принимает значения от 0 до 100, может быть опушенна, 
        в таком случае будет использоваться значение шума заданное в канале  
        :return: Искажённую информацию, представленную в виде массива битов
        """
        randomGenerator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел
        if straight is None: straight = self.noiseProbability
        answer: list = []

        for x in information:
            if randomGenerator.randint(0, 100) < straight:
                answer.append(x * randomGenerator.getrandbits(1))
            else:
                answer.append(x)
        return answer
