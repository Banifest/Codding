# coding=utf-8
# coding=utf-8
import sys
from typing import Optional

from PyQt5.QtWidgets import QApplication, QMessageBox

from src.GUI.controller.coder_controller import CoderController
from src.GUI.controller.test_controller import TestController
from src.GUI.globals_signals import globalSignals
from src.GUI.windows.main_window import MainWindow
from src.coders.abstract_coder import AbstractCoder
# noinspection PyMethodMayBeStatic
from src.helper.error.exception.application_exception import ApplicationException


class MainController:
    firstCoderParams: CoderController
    secondCoderParams: CoderController
    testParams: TestController

    _mainWindow: MainWindow = None

    currentCoder: AbstractCoder = None
    firstCoderForCascade: AbstractCoder = None
    secondCoderForCascade: AbstractCoder = None

    def __init__(self):
        self.firstCoderParams = CoderController()
        self.secondCoderParams = CoderController()
        self.testParams = TestController(
            self.firstCoderParams,
            self.secondCoderParams
        )
        globalSignals.notCorrect.connect(self.error_handle)
        globalSignals.ended.connect(self.finished_test_cycles)
        app = QApplication(sys.argv)
        self._mainWindow = MainWindow(self)
        app.exec()

    @staticmethod
    def error_handle(exception: Optional[ApplicationException]):
        QMessageBox().warning(
            None,
            "Поля заполнены не верной информацией" if exception is None else exception.get_message(),
            "Поля заполнены не верной информацией" if exception is None else exception.get_long_message(),
            QMessageBox.Ok
        )

    def import_from_json(self):
        pass
        # file_path = QFileDialog.getOpenFileName(filter="*.json", parent=self._mainWindow)[0]
        # if file_path != '':
        #     info = json.loads(open(file_path).read())
        # GraphicController().draw_graphic(
        #     info['draw_information'],
        #     info['coder']['name'],
        #     coder_speed=info['coder']['speed'],
        #     start=info['auto_test_information']['start'],
        #     finish=info['auto_test_information']['finish']
        # )

    def finished_test_cycles(self):
        pass
