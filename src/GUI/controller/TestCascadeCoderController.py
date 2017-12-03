from PyQt5.QtWidgets import QWidget

from src.GUI.controller.TestCoderController import TestCoder, TestCoderController
from src.channel.cascade import Cascade
from src.coders.abstractCoder import AbstractCoder
from src.coders.interleaver import Interleaver


class TestCascadeCoderController(TestCoderController):
    def __init__(self, _mainController):
        super().__init__(_mainController)
        self._mainController = _mainController

    def set_thread_class(self):
        self._threadClass = TestCascadeCoder(self._testCoderWindow,
                                             self._mainController.currentCoder,
                                             self._lastResult,
                                             self._mainController.firstCoderForCascade,
                                             self._mainController.secondCoderForCascade)

    def enable_disable_widget(self, param: bool):
        super().enable_disable_widget(param)
        if self._testCoderWindow.is_interleaver_second.isChecked():
            self._testCoderWindow.second_length_text_box.setEnabled(param)
        self._testCoderWindow.is_interleaver_second.setEnabled(param)

    def starting_test(self, param: bool):
        super().starting_test(param)


class TestCascadeCoder(TestCoder):
    def __init__(self, test_window: QWidget, currentCoder: AbstractCoder, lastResult: str,
                 firstCoder: AbstractCoder, secondCoder: AbstractCoder):
        super().__init__(test_window, currentCoder, lastResult)

        self.speed = firstCoder.get_speed() * secondCoder.get_speed()
        self.coderName = 'Каскадный кодер из: {0} и {1}'.format(firstCoder.name, secondCoder.name)
        self.channel = Cascade(
                firstCoder,
                secondCoder,
                self.noiseChance,
                self.countTest,
                False,
                Interleaver.Interleaver(int(test_window.first_length_text_box.text()))
                if test_window.is_interleaver_first.isChecked() else None,
                Interleaver.Interleaver(int(test_window.second_length_text_box.text()))
                if test_window.is_interleaver_second.isChecked() else None)

    def run(self):
        super().run()
