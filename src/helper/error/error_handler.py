# coding=utf-8
from PyQt5.QtWidgets import QWidget, QMessageBox

from src.GUI.globals_signals import globalSignals
from src.helper.error.exception.application_exception import ApplicationException
# noinspection PyMethodMayBeStatic
# Disable for singleton classes
from src.helper.pattern.singleton import Singleton


# noinspection PyMethodMayBeStatic
class ErrorHandler(metaclass=Singleton):
    __UNKNOWN_ERROR: str = "Unknown error"

    def __init__(self):
        pass

    @staticmethod
    def gui_message_box(
            ref_window: QWidget = None,
            rcx_exception: ApplicationException = None,
    ) -> None:
        globalSignals.ended.emit()
        QMessageBox().warning(
            ref_window,
            ErrorHandler.__UNKNOWN_ERROR if rcx_exception is None else rcx_exception.message,
            ErrorHandler.__UNKNOWN_ERROR if rcx_exception is None else rcx_exception.long_message,
            QMessageBox.Ok
        )