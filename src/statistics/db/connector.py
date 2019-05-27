# coding=utf-8
from typing import Optional

from sqlalchemy import create_engine
# Need for hints
# noinspection PyProtectedMember
from sqlalchemy.engine import Connection, Engine

from src.config.config_processor import ConfigProcessor
from src.helper.pattern.singleton import Singleton


class Connector(metaclass=Singleton):
    _connection: Connection = None
    _engine: Engine = None

    def get_connection(
            self,
            login: Optional[str] = None,
            password: Optional[str] = None,
    ) -> Connection:
        """
        Method for getting connection to native(remote) database
        :param login: login for user of database
        :param password: password for user of database
        :return: Connection object
        """
        if login is None:
            login = ConfigProcessor().config.db_setting.login
        if password is None:
            password = ConfigProcessor().config.db_setting.password

        if self._connection is None:
            self._connection = self.get_engine(login, password).connect()

        return self._connection

    def get_engine(
            self,
            login: Optional[str] = None,
            password: Optional[str] = None,
    ) -> Engine:
        """
        Method for getting engine to remote database Heroku
        :param login: login for user of database
        :param password: password for user of database
        :return: Engine object
        """
        if login is None or login == '':
            login = ConfigProcessor().config.db_setting.login
        if password is None or password == '':
            password = ConfigProcessor().config.db_setting.password

        if self._engine is None:
            # This is connection string. This statement shouldn't checked
            # noinspection SpellCheckingInspection
            self._engine = create_engine(
                "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
                    login,
                    password,
                    ConfigProcessor().config.db_setting.address,
                    ConfigProcessor().config.db_setting.port,
                    ConfigProcessor().config.db_setting.database_name,
                ), echo=False
            )
        return self._engine

    def save(self):
        self._connection.query("COMMIT")
