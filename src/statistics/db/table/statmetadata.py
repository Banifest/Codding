# coding=utf-8
import uuid

from sqlalchemy import MetaData

from src.helper.pattern.singleton import Singleton


def process_result_value(self, value, dialect):
    if value is None:
        return value
    else:
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value


class StatMetaData(metaclass=Singleton):
    _metadata: MetaData = None

    def __init__(self):
        self._metadata = None

    def get_metadata(self):
        if self._metadata is None:
            self._metadata = MetaData()
        return self._metadata
