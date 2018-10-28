from PyQt5.QtWidgets import QWidget, QMessageBox

from src.helper.error.exception.ApplicationException import ApplicationException


class ErrorHandler:
    __ref_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__ref_instance is None:
            cls.__ref_instance = cls.__init__()

        return cls.__ref_instance

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
