# coding=utf-8
# coding=utf-8
import logging
import os

from src.helper.pattern.singleton import Singleton


class Logger(logging.Logger, metaclass=Singleton):
    def __init__(self):
        super().__init__("AppLogger")
        self.setLevel("DEBUG")

        if os.path.exists("log.txt"):
            os.remove("log.txt")
        handler = logging.FileHandler("log.txt", encoding='UTF-8')

        handler.setLevel("DEBUG")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        self.addHandler(handler)


log = Logger()
