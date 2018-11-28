# coding=utf-8
from PyQt5.QtWidgets import QWidget, QMessageBox

from src.helper.error.exception.application_exception import ApplicationException
# noinspection PyMethodMayBeStatic
# Disable for singleton classes
from src.helper.pattern.singleton import Singleton


# noinspection PyMethodMayBeStatic
class ErrorHandler(metaclass=Singleton):
    def __init__(self):
        pass

    def gui_message_box(
            self,
            ref_window: QWidget = None,
            rcx_exception: ApplicationException = None,
            str_message_title: str = "",
            str_message_text: str = ""
    ) -> None:
        QMessageBox().warning(
            QWidget=ref_window,
            p_str=rcx_exception.get_message() if rcx_exception is not None else str_message_title,
            p_str_1=rcx_exception.get_long_message() if rcx_exception is not None else str_message_text,
            buttons=QMessageBox.Ok
        )
