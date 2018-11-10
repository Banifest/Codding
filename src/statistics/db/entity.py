from abc import abstractmethod

from postgresql.driver.pq3 import Connector

from src.statistics.db.connector import Connector as Conn


class Entity:
    _connection: Connector = Conn().get_connection()

    _prepare_selection_statement = _connection.prepare("""
        SELECT *
        FROM $1        
    """)

    def __init__(self):
        _connection = Conn().get_connection()

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def read(self):
        pass

    def save(self):
        self._connection.commit()
