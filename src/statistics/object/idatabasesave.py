# coding=utf-8
import uuid
from abc import abstractmethod, ABCMeta


class IDataBaseSave(metaclass=ABCMeta):

    @abstractmethod
    def save_to_database(self, coder_guid: uuid.UUID):
        pass
