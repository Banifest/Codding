# coding=utf-8
# coding=utf-8
import json
import sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from src.GUI.controller.CoderController import CoderParams
from src.GUI.controller.TestController import TestController
from src.GUI.globals_signals import globalSignals
from src.GUI.graphics import draw_graphic
from src.GUI.windows.MainWindow import MainWindow
from src.coders.abstractCoder import AbstractCoder


class MainController:
    firstCoderParams: CoderParams
    secondCoderParams: CoderParams
    testParams: TestController

    _mainWindow: MainWindow = None

    currentCoder: AbstractCoder = None
    firstCoderForCascade: AbstractCoder = None
    secondCoderForCascade: AbstractCoder = None

    def __init__(self):
        self.firstCoderParams = CoderParams()
        self.secondCoderParams = CoderParams()
        self.testParams = TestController(self.firstCoderParams,
                                         self.secondCoderParams)
        globalSignals.notCorrect.connect(self.error_handle)
        app = QApplication(sys.argv)
        self._mainWindow = MainWindow(self)
        app.exec()

    def error_handle(self):
        QMessageBox.warning(
            None,
            "Поля заполнены не верной информацией",
            "Поля заполнены не верной информацией",
            QMessageBox.Ok
        )

    def import_from_json(self):
        file_path = QFileDialog.getOpenFileName(filter="*.json", parent=self._mainWindow)[0]
        if file_path != '':
            info = json.loads(open(file_path, "r").read())
            draw_graphic(
                info['draw_information'],
                info['coder']['name'],
                coder_speed=info['coder']['speed'],
                start=info['auto_test_information']['start'],
                finish=info['auto_test_information']['finish']
            )
