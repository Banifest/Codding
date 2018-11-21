# coding=utf-8
from typing import Optional

from sqlalchemy import create_engine

from src.helper.pattern.singleton import Singleton


class Connector(metaclass=Singleton):
    __ref_instance = None
    _connection = None
    _engine = None

    def __init__(self):
        pass

    def get_connection(
            self,
            login: Optional[str] = "mjdlelvwwraanx",
            password: Optional[str] = "089bf6255905ba11b1fb462a2d0177204a3b6d6f93c7fb989a721b6686d26a1b"
    ):
        """
        Method for getting connection to remote database Heroku
        :param login: login for user of database
        :param password: password for user of database
        :return: Connection object
        """
        if self._connection is None:
            self._connection = self.get_engine(login, password).connect()

        return self._connection

    def get_engine(
            self,
            login: Optional[str] = "mjdlelvwwraanx",
            password: Optional[str] = "089bf6255905ba11b1fb462a2d0177204a3b6d6f93c7fb989a721b6686d26a1b"
    ):
        """
        Method for getting engine to remote database Heroku
        :param login: login for user of database
        :param password: password for user of database
        :return: Engine object
        """
        if self._engine is None:
            self._engine = create_engine(
                "postgres://{0}:{1}@ec2-54-246-85-234.eu-west-1.compute.amazonaws.com:5432/d32aj68h32vv4c".format(
                    login,
                    password
                ),
                connect_args={
                    'sslmode': 'require'
                }
            )
            return self._engine

    def save(self):
        self._connection.query("COMMIT")
