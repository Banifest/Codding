#!usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication

from src.GUI.windows.MainWindow import MainWindow
from src.logger import log


if __name__ == '__main__':
    # coder = LubyTransform.Coder(3,4,10)
    # print(coder.Decoding(coder.Encoding([0,1,1,1,0,1,0,1])))
    try:
        log.info("Начало работы программы")
        App = QApplication(sys.argv)
        window = MainWindow()
        App.exec()
        log.info("Конец работы программы")
    except Exception as e:
        print(e)
        log.critical("Необрабатываемое исключение")
else:
    raise Exception("Невозможен import данного файла:(")
