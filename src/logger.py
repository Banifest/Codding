# coding=utf-8
import logging
import os
import uuid

from src.helper.pattern.singleton import Singleton


class Logger(logging.Logger, metaclass=Singleton):
    def __init__(self):
        super().__init__("AppLogger")
        self.setLevel("DEBUG")

        log_guid = uuid.uuid4()

        if not os.path.exists("log/"):
            os.makedirs("log")

        if os.path.exists("log/log{0}.txt".format(log_guid)):
            os.remove("log/log{0}.txt".format(log_guid))
        handler = logging.FileHandler("log/log{0}.txt".format(log_guid), encoding='UTF-8')

        handler.setLevel("DEBUG")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        self.addHandler(handler)


log = Logger()
