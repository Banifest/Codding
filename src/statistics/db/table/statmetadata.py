# coding=utf-8
from sqlalchemy import MetaData

from helper.pattern.singleton import Singleton


class StatMetaData(metaclass=Singleton):
    _metadata: MetaData

    def get_metadata(self):
        if self._metadata is None:
            self._metadata = MetaData()
        return self._metadata
