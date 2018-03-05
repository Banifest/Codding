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
                                             self._mainController.secondCoderForCascade,
                                             start=self.start,
                                             finish=self.finish)

    def enable_disable_widget(self, param: bool):
        super().enable_disable_widget(param)
        if self._testCoderWindow.is_interleaver_second.isChecked():
            self._testCoderWindow.second_length_text_box.setEnabled(param)
        self._testCoderWindow.is_interleaver_second.setEnabled(param)

    def starting_test(self, param: bool):
        super().starting_test(param)


class TestCascadeCoder(TestCoder):
    def __init__(self, test_window: QWidget, currentCoder: AbstractCoder, lastResult: str,
                 firstCoder: AbstractCoder, secondCoder: AbstractCoder,
                 start: float, finish: float):
        super().__init__(test_window, currentCoder, lastResult, start, finish)

        self.coderSpeed = firstCoder.get_speed() * secondCoder.get_speed()
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
        self.information_dict['is_cascade'] = True
        super().run()
        self.information_dict['coder'] = {
            'first_coder': self.channel.firstCoder.to_json(),
            'second_coder': self.channel.secondCoder.to_json(),
            'name': self.coderName,
            'speed': self.coderSpeed
        }
