class Interleaver:
    lengthSmashing: int

    def __init__(self, lengthSmashing: int):
        self.lengthSmashing = lengthSmashing

    def Shuffle(self, information: list) -> list:
        answer: list = []
        for x in range(self.lengthSmashing):
            isEnd: bool = False
            counter: int = 0
            while not isEnd:
                if (counter * self.lengthSmashing + x) < len(information):
                    answer.append(information[counter * self.lengthSmashing + x])
                else:
                    isEnd = True
                counter += 1
        return answer
