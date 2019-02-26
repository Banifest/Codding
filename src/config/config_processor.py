# coding=utf-8
import os

import jsonpickle

from src.config.config import Config
from src.helper.pattern.singleton import Singleton


class ConfigProcessor(metaclass=Singleton):
    _config: Config
    CONFIG_FILE_NAME: str = "config.json"

    def __init__(self):
        self._config = Config()

    def create_standard_config(self):
        config_file = open(ConfigProcessor.CONFIG_FILE_NAME, mode="w")
        config_file.write(jsonpickle.encode(self._config, unpicklable=False))
        config_file.close()

    def get_config(self) -> Config:
        return self._config

    def parse_config(self):
        if os.path.exists(ConfigProcessor.CONFIG_FILE_NAME):
            config_file = open(ConfigProcessor.CONFIG_FILE_NAME)
            self._config = jsonpickle.decode(config_file.read())
            config_file.close()
        else:
            self.create_standard_config()
