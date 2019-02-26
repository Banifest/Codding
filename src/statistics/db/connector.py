# coding=utf-8
from typing import Optional

from sqlalchemy import create_engine

from src.config.config_processor import ConfigProcessor
from src.helper.pattern.singleton import Singleton


class Connector(metaclass=Singleton):
    __ref_instance = None
    _connection = None
    _engine = None

    def __init__(self):
        pass

    def get_connection(
            self,
            login: Optional[str] = ConfigProcessor().get_config().db_setting.login,
            password: Optional[str] = ConfigProcessor().get_config().db_setting.password,
    ):
        """
        Method for getting connection to native(remote) database
        :param login: login for user of database
        :param password: password for user of database
        :return: Connection object
        """
        if self._connection is None:
            self._connection = self.get_engine(login, password).connect()

        return self._connection

    def get_engine(
            self,
            login: Optional[str] = ConfigProcessor().get_config().db_setting.login,
            password: Optional[str] = ConfigProcessor().get_config().db_setting.password,
    ):
        """
        Method for getting engine to remote database Heroku
        :param login: login for user of database
        :param password: password for user of database
        :return: Engine object
        """
        if self._engine is None:
            self._engine = create_engine(
                "postgres://{0}:{1}@localhost:5433/postgres".format(
                    login,
                    password
                ), echo=True
            )
        return self._engine

    def save(self):
        self._connection.query("COMMIT")
