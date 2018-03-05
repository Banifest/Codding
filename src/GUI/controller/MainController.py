import json
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog

from src.GUI.controller.AboutCoderController import AboutCoderController
from src.GUI.controller.CoderController import CoderParams
from src.GUI.controller.TestCascadeCoderController import TestCascadeCoderController
from src.GUI.controller.TestCoderController import TestCoderController
from src.GUI.graphics import draw_graphic
from src.GUI.windows.AboutCoderWindow import AboutCoderWindow
from src.GUI.windows.AddCoderWindow import AddCoderWindow
from src.GUI.windows.MainWindow import MainWindow
from src.GUI.windows.TestCascadeCoderWindow import TestCascadeCoderWindow
from src.GUI.windows.TestCoderWindow import TestCoderWindow
from src.coders.abstractCoder import AbstractCoder
# noinspection PyAttributeOutsideInit
from src.coders.casts import StrListToList
# noinspection PyAttributeOutsideInit
from src.coders.convolutional.Coder import Coder as ConvolutionalCoder
from src.coders.convolutional.CoderForPacket import ConvolutionalCoderForPacket
from src.coders.cyclical.Coder import Coder as CyclicalCoder
# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
from src.coders.fountain.LubyTransform import Coder as LubyTransform
from src.coders.linear.ReedMuller import Coder as ReedMullerCoder
from src.coders.linear.hemming import Coder as HemmingCoder


# noinspection PyAttributeOutsideInit,PyCallByClass
class MainController:
    firstCoderParams: CoderParams
    secondCoderParams: CoderParams

    _mainWindow: MainWindow = None
    _addCoderWindow: AddCoderWindow = None
    _testCascadeCoderController: TestCascadeCoderController = None
    _testSimpleCoderController: TestCoderController = None
    _testCascadeCoderWindow: TestCascadeCoderWindow = None
    _testSimpleCoderWindow: TestCoderWindow = None
    _dialogAboutCoderController: AboutCoderController = None
    _dialogAboutCoderWindow: AboutCoderWindow = None

    currentCoder: AbstractCoder = None
    firstCoderForCascade: AbstractCoder = None
    secondCoderForCascade: AbstractCoder = None

    def __init__(self):
        self.firstCoderParams = CoderParams()
        self.secondCoderParams = CoderParams()

        app = QApplication(sys.argv)
        self._mainWindow = MainWindow(self)
        app.exec()


    def import_from_json(self):
        filePath = QFileDialog.getOpenFileName(filter="*.json", parent=self._mainWindow)[0]
        if filePath != '':
            info = json.loads(open(filePath, "r").read())
            draw_graphic(info['draw_information'],
                         info['coder']['name'],
                         coder_speed=info['coder']['speed'],
                         start=info['auto_test_information']['start'],
                         finish=info['auto_test_information']['finish'])


    def del_add_coder_window(self):
        if self._addCoderWindow is not None:
            del self._addCoderWindow

    def del_test_simple_coder_window(self):
        if self._testSimpleCoderWindow is not None:
            del self._testSimpleCoderWindow

    def del_test_cascade_coder_window(self):
        if self._testCascadeCoderWindow is not None:
            del self._testCascadeCoderWindow
