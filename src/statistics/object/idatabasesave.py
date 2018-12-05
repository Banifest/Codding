# coding=utf-8
from abc import abstractmethod, ABCMeta


class IDataBaseSave(metaclass=ABCMeta):

    @abstractmethod
    def save_to_database(self):
        pass
