# coding=utf-8
import os
from typing import Optional

import jsonpickle

from src.config.config import Config
from src.helper.pattern.singleton import Singleton


class ConfigProcessor(metaclass=Singleton):
    _config: Config

    __CURRENT_DIR: str = ".\\"
    __CONFIG_FILE_NAME: str = "config.json"
    __DB_CONFIG: str = "db_setting"
    __GRAPHIC_CONFIG: str = "graphic_setting"

    def __init__(self):
        self._config = Config()

    def _create_standard_config(self, file_path: str):
        config_file = open(file_path, mode="w")
        config_file.write(jsonpickle.encode(self._config, unpicklable=False))
        config_file.close()

    @property
    def config(self) -> Config:
        return self._config

    def parse_config(self, file_path: Optional[str] = None):
        local_file_path: str = "{0}{1}".format(file_path or self.__CURRENT_DIR, self.__CONFIG_FILE_NAME)
        if os.path.exists(local_file_path):
            config_file = open(local_file_path)
            parsed_config = jsonpickle.decode(config_file.read())
            self._config.db_setting = Config.DBSetting(**parsed_config[ConfigProcessor.__DB_CONFIG])
            self._config.graphic_setting = Config.GraphicSetting(**parsed_config[ConfigProcessor.__GRAPHIC_CONFIG])
            config_file.close()
        else:
            self._create_standard_config(file_path=local_file_path)
