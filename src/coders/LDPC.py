from src.coders import abstractCoder


class Coder(abstractCoder.Coder):
    matrixTransformation: list = []

    def __init__(self, length_information: int):
        pass

    def Encoding(self, information: list) -> list:
        pass


    def Decoding(self, information: list) -> list:
        pass
