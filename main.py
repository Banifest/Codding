# coding=utf-8
# coding=utf-8
from src.GUI.controller.MainController import MainController

from src.logger import log

if __name__ == '__main__':
    try:
        log.info("Start program")
        controller = MainController()
        log.info("End program")
    except Exception as e:
        print(e)
        log.critical("Unhandled exception")
else:
    raise Exception("Невозможен import данного файла:(")
