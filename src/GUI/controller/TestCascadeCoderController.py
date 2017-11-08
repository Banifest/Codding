from PyQt5.QtWidgets import QWidget

from GUI.controller.TestCoderController import TestCoder, TestCoderController
from channel.cascade import Cascade
from coders.abstractCoder import AbstractCoder
from coders.interleaver import Interleaver


class TestCascadeCoderController(TestCoderController):
    def __init__(self, _mainController):
        super().__init__(_mainController)

    def enable_disable_widget(self, param: bool):
        super().enable_disable_widget(param)
        self._testCoderWindow.second_length_text_box.setEnabled(param)
        self._testCoderWindow.is_interleaver_second.setEnabled(param)


class TestCascadeCoder(TestCoder):
    def __init__(self, test_window: QWidget, currentCoder: AbstractCoder, lastResult: str):
        super().__init__(test_window, currentCoder, lastResult)

        self.channel = Cascade(
                self._mainController.firstCoderForCascade,
                self._mainController.secondCoderForCascade,
                self.noiseChance,
                self.countTest,
                False,
                Interleaver.Interleaver(int(
                    test_window.first_length_text_box.text())) if test_window.is_interleaver_first.isEnabled() else None,
                Interleaver.Interleaver(int(
                    test_window.second_length_text_box.text())) if test_window.is_interleaver_second.isEnabled() else None)
