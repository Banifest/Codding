# coding=utf-8
import uuid
from abc import abstractmethod, ABCMeta


class IDataBaseSerialize(metaclass=ABCMeta):

    @abstractmethod
    def save_to_database(self, coder_guid: uuid.UUID):
        pass
