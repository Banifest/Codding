from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QProgressBar

from GUI.windows.TestCoderWindow import TestCoderWindow


# noinspection PyAttributeOutsideInit
class TestCoderController:
    testCoderWindow: TestCoderWindow

    def set_window(self, testCoderWindow):
        self.testCoderWindow = testCoderWindow

    def starting_test(self):
        TestCoder(self.testCoderWindow.single_test)


class TestCoder(QThread):
    first_progress_bar: QProgressBar

    def __init__(self, first_progress_bar: QProgressBar):
        QThread.__init__(self)
        self.first_progress_bar = first_progress_bar

    def __del__(self):
        self.wait()

    def run(self):
        pass
