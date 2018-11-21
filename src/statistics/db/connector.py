# coding=utf-8
from typing import Optional

import postgresql
from itypes import Object
from postgresql import driver

from src.helper.pattern.singleton import Singleton


class Connector(metaclass=Singleton):
    __ref_instance = None
    # Connection
    _connection = None
    _egine: Object
    _egine_connection: Object

    def __init__(self):
        pass

    def get_connection(self, login: Optional[str] = "postgres", password: Optional[str] = "admin") \
            -> driver.pq3.Connector:

        if self._connection is None:
            self._connection = postgresql.open('pq://{0}:{1}@localhost:5433/postgres'.format(
                login,
                password
            ))
        return self._connection

    def save(self):
        self._connection.query("COMMIT")
