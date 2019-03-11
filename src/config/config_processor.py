# coding=utf-8
import os

import jsonpickle

from src.config.config import Config
from src.helper.pattern.singleton import Singleton


class ConfigProcessor(metaclass=Singleton):
    _config: Config

    __CONFIG_FILE_NAME: str = "config.json"
    __DB_CONFIG: str = "db_setting"
    __GRAPHIC_CONFIG: str = "graphic_setting"

    def __init__(self):
        self._config = Config()

    def create_standard_config(self):
        config_file = open(ConfigProcessor.__CONFIG_FILE_NAME, mode="w")
        config_file.write(jsonpickle.encode(self._config, unpicklable=False))
        config_file.close()

    @property
    def config(self) -> Config:
        return self._config

    def parse_config(self):
        if os.path.exists(ConfigProcessor.__CONFIG_FILE_NAME):
            config_file = open(ConfigProcessor.__CONFIG_FILE_NAME)
            parsed_config = jsonpickle.decode(config_file.read())
            self._config.db_setting = Config.DBSetting(**parsed_config[ConfigProcessor.__DB_CONFIG])
            self._config.graphic_setting = Config.GraphicSetting(**parsed_config[ConfigProcessor.__GRAPHIC_CONFIG])
            config_file.close()
        else:
            self.create_standard_config()
