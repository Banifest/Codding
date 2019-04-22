# coding=utf-8
from PyQt5.QtCore import pyqtSignal, QObject


class __GlobalSignals(QObject):
    startTesting = pyqtSignal('bool')
    stepFinished = pyqtSignal('int')
    autoStepFinished = pyqtSignal('int')
    ended = pyqtSignal()
    notCorrect = pyqtSignal(object)
    lockStart = pyqtSignal()
    unlockStart = pyqtSignal()


globalSignals = __GlobalSignals()
__all__ = [globalSignals]
