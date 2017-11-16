import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from GUI.controller.AboutCoderController import AboutCoderController
from GUI.controller.TestCascadeCoderController import TestCascadeCoderController
from GUI.controller.TestCoderController import TestCoderController
from GUI.windows.AboutCoderWindow import AboutCoderWindow
from GUI.windows.AddCoderWindow import AddCoderWindow
from GUI.windows.MainWindow import MainWindow
from GUI.windows.TestCascadeCoderWindow import TestCascadeCoderWindow
from GUI.windows.TestCoderWindow import TestCoderWindow
from coders.abstractCoder import AbstractCoder
# noinspection PyAttributeOutsideInit
from coders.casts import StrListToList
# noinspection PyAttributeOutsideInit
from coders.convolutional.Coder import Coder as ConvolutionalCoder
from coders.convolutional.CoderForPacket import ConvolutionalCoderForPacket
from coders.cyclical.Coder import Coder as CyclicalCoder
# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
from coders.fountain.LubyTransform import Coder as LubyTransform
from coders.linear.ReedMuller import Coder as ReedMullerCoder
from coders.linear.hemming import Coder as HemmingCoder


# noinspection PyAttributeOutsideInit
class MainController:
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
        App = QApplication(sys.argv)
        self._mainWindow = MainWindow(self)
        App.exec()

    def set_coder(self):
        coder_name = self._addCoderWindow.choose_comboBox.currentText()
        try:
            if coder_name == "Хемминга":
                self.currentCoder = HemmingCoder(int(self._addCoderWindow.sizePackageTextBox.text()))
            elif coder_name == "Циклический":
                self.currentCoder = CyclicalCoder(
                        int(self._addCoderWindow.sizePackageTextBox.text()),
                        int(self._addCoderWindow.listPolynomialTextBox.text())
                        )
            elif coder_name == 'Сверточный':
                self.currentCoder = ConvolutionalCoder(
                        StrListToList(self._addCoderWindow.listPolynomialTextBox.text()),
                        1,
                        int(len(StrListToList(self._addCoderWindow.listPolynomialTextBox.text()))),
                        int(self._addCoderWindow.countMemoryRegistersTextBox.text())
                        )
            elif coder_name == "Фонтанный":
                self.currentCoder = LubyTransform(
                        int(self._addCoderWindow.sizeBlockTextBox.text()),
                        int(self._addCoderWindow.countBlocksTextBox.text()),
                        int(self._addCoderWindow.sizePackageTextBox.text())
                        )
            elif coder_name == 'Рида-Маллера':
                self.currentCoder = ReedMullerCoder(
                        int(self._addCoderWindow.sizePackageTextBox.text()),
                        int(self._addCoderWindow.powerReedMullerTextBox.text())
                        )
            elif coder_name == 'Сверточный для пакетов':
                self.currentCoder = ConvolutionalCoderForPacket(
                        StrListToList(self._addCoderWindow.listPolynomialTextBox.text()),
                        1,
                        int(len(StrListToList(self._addCoderWindow.listPolynomialTextBox.text()))),
                        int(self._addCoderWindow.countMemoryRegistersTextBox.text()),
                        int(self._addCoderWindow.powerReedMullerTextBox.text())
                        )

            if self._addCoderWindow.first_coder_radio_button.isChecked():
                self.firstCoderForCascade = self.currentCoder
            else:
                self.secondCoderForCascade = self.currentCoder

            del self._addCoderWindow
        except:
            QMessageBox.warning(self._addCoderWindow,
                                "Поля заполнены не верной информацией",
                                "Поля заполнены не верной информацией",
                                QMessageBox.Ok
                                )

    def set_test_coder_window(self):
        if self.currentCoder is not None:
            self._testSimpleCoderController = TestCoderController(self)
            self._testSimpleCoderWindow = TestCoderWindow(self._testSimpleCoderController)
        else:
            QMessageBox.warning(self._mainWindow,
                                "Не был создан ни один кодер",
                                "Не был создан ни один кодер",
                                QMessageBox.Ok
                                )

    def set_create_coder_window(self):
        self._addCoderWindow = AddCoderWindow(self)

    def set_test_cascade_coder_window(self):
        if self.firstCoderForCascade is not None and self.secondCoderForCascade is not None:
            self._testCascadeCoderController = TestCascadeCoderController(self)
            self._testCascadeCoderWindow = TestCascadeCoderWindow(self._testCascadeCoderController)
        else:
            QMessageBox.warning(self._mainWindow,
                                "Не были созданы кодеры",
                                "Не были созданы кодеры",
                                QMessageBox.Ok)

    def set_about_coder_dialog(self):
        if self.currentCoder is not None:
            self._dialogAboutCoderController = AboutCoderController(self)
            self._dialogAboutCoderWindow = AboutCoderWindow(self._dialogAboutCoderController)
        else:
            QMessageBox.warning(self._mainWindow,
                                "Не были созданы кодеры",
                                "Не были созданы кодеры",
                                QMessageBox.Ok)

    def del_add_coder_window(self):
        if self._addCoderWindow is not None:
            del self._addCoderWindow

    def del_test_simple_coder_window(self):
        if self._testSimpleCoderWindow is not None:
            del self._testSimpleCoderWindow

    def del_test_cascade_coder_window(self):
        if self._testCascadeCoderWindow is not None:
            del self._testCascadeCoderWindow
