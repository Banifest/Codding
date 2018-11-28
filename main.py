# coding=utf-8
from src.GUI.controller.MainController import MainController
from src.endpoint.console.Parser import Parser
from src.endpoint.console.enum_app_mode import EnumAppMode
from src.logger import log

if __name__ == '__main__':
    if Parser().get_app_mode == EnumAppMode.GUI:
        try:
            log.info("Start program")
            controller = MainController()
            log.info("End program")
        except Exception as e:
            print(e)
            log.critical("Unhandled exception")
else:
    raise Exception("Невозможен import данного файла:(")
