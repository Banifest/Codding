# coding=utf-8
from src.GUI.controller.main_controller import MainController
from src.config.config_processor import ConfigProcessor
from src.endpoint.console.app_parser import AppParser
from src.endpoint.console.enum_app_mode import EnumAppMode
from src.helper.error.exception.application_exception import ApplicationException
from src.logger import log

if __name__ == '__main__':
    ConfigProcessor().parse_config()
    if AppParser().app_mode == EnumAppMode.GUI:
        try:
            log.info("Start program")
            controller = MainController()
            log.info("End program")
        except Exception as e:
            print(e)
            log.critical("Unhandled exception")
else:
    raise ApplicationException("It isn't module")
