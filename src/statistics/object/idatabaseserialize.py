# coding=utf-8
import uuid
from abc import ABC, abstractmethod

from sqlalchemy.engine import Connection


class IDataBaseSerialize(ABC):

    @abstractmethod
    def save_to_database(self, coder_guid: uuid.UUID, connection: Connection):
        raise NotImplementedError()
