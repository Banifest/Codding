# coding=utf-8

from src.GUI.controller.main_controller import MainController
from src.config.config_processor import ConfigProcessor
from src.endpoint.console.app_parser import AppParser
from src.endpoint.console.console_processor import ConsoleProcessor
from src.endpoint.console.enum_app_mode import EnumAppMode
from src.helper.error.exception.application_exception import ApplicationException
from src.logger import log

if __name__ == '__main__':
    ConfigProcessor().parse_config()
    try:
        log.info("Start program")
        if AppParser().app_mode == EnumAppMode.GUI:
            log.info("GUI mode")
            controller = MainController()
        elif AppParser().app_mode == EnumAppMode.CONSOLE:
            log.info("Console mode")
            ConsoleProcessor().transfer()
        log.info("End program")
    except Exception as error:
        print(error)
        log.critical("Unhandled exception")
else:
    raise ApplicationException("Cannot be import this as module ({0})".format(__file__))
