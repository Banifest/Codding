from PyQt5.QtCore.QJsonValue import Object
from PyQt5.QtWidgets import QWidget, QMessageBox


class ErrorHandler:
    __ref_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__ref_instance is None:
            cls.__ref_instance = cls.__init__()

        return cls.__ref_instance

    def __init__(self):
        pass

    def gui_message_box(self, window: QWidget = None, exception: Object = None, title: str = "",
                        message_text: str = ""):
        QMessageBox.warning(
            QWidget=window,
            "Поля заполнены не верной информацией",
            "Поля заполнены не верной информацией",
            buttons=QMessageBox.Ok
        )
