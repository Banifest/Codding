from postgresql.driver.pq3 import Connector

from src.statistics.db.connector import Connector as Conn


class Entity:
    _connection: Connector = Conn().get_connection()

    def __init__(self):
        _connection = Conn().get_connection()

    def create(self):
        pass

    def delete(self):
        pass

    def read(self):
        pass
