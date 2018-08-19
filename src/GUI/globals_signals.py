# coding=utf-8
# coding=utf-8
from PyQt5.QtCore import pyqtSignal, QObject


class GlobalSignals(QObject):
    stepFinished = pyqtSignal('int')
    autoStepFinished = pyqtSignal('int')
    ended = pyqtSignal()
    notCorrect = pyqtSignal()


globalSignals = GlobalSignals()
__all__ = [globalSignals]
