from src.coders import abstractCoder


class Coder(abstractCoder.Coder):
    """
    Для хранения матриц большого размера будем использовать граф
    где columns список верхних вершин, а lines нижних. В каждом элементе
    списка хранится список связаных с ребрами противоположных вершин
    (в columns с lines, а в lines с columns)
    """
    columns: list = []
    lines: list = []

    matrixTransformation: list = []

    def __init__(self, n: int, k: int):
        """
        Args:
            n: int количество битов в пакете
            k: int количество битов передаваемой информации
        """
        self.n = n
        self.k = k

    def Encoding(self, information: list) -> list:
        # TODO генерация проверочной матрицы и заполнение графа
        #
        #
        pass


    def Decoding(self, information: list) -> list:
        pass
