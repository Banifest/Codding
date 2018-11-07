from src.statistics.db.connector import Connector


class Entity:
    _connection = Connector().get_connection()

    def __init__(self):
        _connection = Connector().get_connection()

    def create(self):
        pass

    def delete(self):
        pass

    def read(self):
        pass
