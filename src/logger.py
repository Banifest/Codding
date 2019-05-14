# coding=utf-8
import datetime
import logging
import os

from src.helper.pattern.singleton import Singleton


class __Logger(logging.Logger, metaclass=Singleton):
    def __init__(self):
        super().__init__("AppLogger")
        self.setLevel("DEBUG")

        log_crt_timestamp = str(datetime.datetime.now())
        log_full_name = ("log\\log_{0}.log".format(log_crt_timestamp)).replace(" ", "").replace(":", "-")

        if not os.path.exists("log\\"):
            os.makedirs("log")

        if os.path.exists(log_full_name):
            os.remove(log_full_name)
        handler = logging.FileHandler(filename=log_full_name, encoding='UTF-8')

        handler.setLevel("DEBUG")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        self.addHandler(handler)


log = __Logger()
