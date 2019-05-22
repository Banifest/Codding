# coding=utf-8

from sqlalchemy import MetaData

from src.helper.pattern.singleton import Singleton


class StatMetaData(metaclass=Singleton):
    _metadata: MetaData = None

    def __init__(self):
        self._metadata = MetaData()

    @property
    def metadata(self) -> MetaData:
        return self._metadata
