# coding=utf-8
import numpy as np

from src.coders import abstract_coder


class Coder(abstract_coder.AbstractCoder):
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
        # TODO генерация проверочной матрицы и заполнение графа
        #
        #
        np.array()


    def encoding(self, information: list) -> list:

        pass


    def decoding(self, information: list) -> list:
        pass
