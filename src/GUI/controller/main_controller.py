# coding=utf-8
# coding=utf-8
import json
import sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from src.GUI.controller.coder_controller import CoderController
from src.GUI.controller.test_controller import TestController
from src.GUI.globals_signals import globalSignals
from src.GUI.graphics import GraphicController
from src.GUI.windows.main_window import MainWindow
from src.coders.abstract_coder import AbstractCoder


# noinspection PyMethodMayBeStatic
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

    def error_handle(self):
        QMessageBox().warning(
            None,
            "Поля заполнены не верной информацией",
            "Поля заполнены не верной информацией",
            QMessageBox.Ok
        )

    def import_from_json(self):
        file_path = QFileDialog.getOpenFileName(filter="*.json", parent=self._mainWindow)[0]
        if file_path != '':
            info = json.loads(open(file_path).read())
            GraphicController().draw_graphic(
                info['draw_information'],
                info['coder']['name'],
                coder_speed=info['coder']['speed'],
                start=info['auto_test_information']['start'],
                finish=info['auto_test_information']['finish']
            )

    def finished_test_cycles(self):
        pass
