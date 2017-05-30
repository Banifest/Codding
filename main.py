#!usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication

from src.GUI.windows.MainWindow import MainWindow
from src.coders import convolutional
from src.coders.casts import BitListToInt
from src.logger import log


if __name__ == '__main__':
    a = convolutional.Coder.Coder(2, [1, 3], 1, 2, 2)
    test = [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0]
    print(a.Encoding(test))
    print(BitListToInt(test))
    print(BitListToInt(a.Decoding([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1])))
    b = [1, 1, 0, 1]
    a.Decoding(b)
    try:
        log.info("Начало работы программы")
        App = QApplication(sys.argv)
        window = MainWindow()
        App.exec()
        log.info("Конец работы программы")
    except Exception as e:
        print(e)
        log.critical("Необрабатываемое исключение")
        pass
else:
    raise Exception("Невозможен import данного файла:(")
