from PyQt5.QtWidgets import QProgressBar

from src.GUI.controller import CoderController
from src.GUI.controller.ThreadControllers import TestCoder, TestCascadeCoder


class TestController:
    _firstCoderParams: CoderController
    _secondCoderParams: CoderController

    _firstThreadClass: TestCoder
    _cascadeThreadClass: TestCascadeCoder

    _singleProgress: QProgressBar
    _autoProgress: QProgressBar

    noiseStart: float = 1.0
    noiseEnd: float = 2.0
    countTest: int = 100
    testInfo: int = 985

    _test_type: int = 0

    def __init__(self,
                 first_coder_params: CoderController,
                 second_coder_params: CoderController,
                 ):
        self._firstCoderParams = first_coder_params
        self._secondCoderParams = second_coder_params

    def set_single_progress(self, single_progress: QProgressBar) -> None:
        self._singleProgress = single_progress

    def set_auto_progress(self, auto_progress: QProgressBar) -> None:
        self._autoProgress = auto_progress

    def set_noise_start(self, value: float) -> None:
        self.noiseStart = value

    def set_noise_end(self, value: float) -> None:
        self.noiseEnd = value

    def set_count_test(self, value: int) -> None:
        self.countTest = value

    def set_test_info(self, value: int) -> None:
        self.testInfo = value

    def set_first_coder_thread_class(self):
        self._firstThreadClass = TestCoder(self.noiseStart,
                                           self.countTest,
                                           self.testInfo,
                                           self._firstCoderParams.coder,
                                           '',
                                           start=self.noiseStart,
                                           finish=self.noiseEnd)

    def set_cascade_coder_thread_class(self):
        self._cascadeThreadClass = TestCascadeCoder(
                self.noiseStart,
                self.countTest,
                self.testInfo,
                self._firstCoderParams.coder,
                self._firstCoderParams.coder,
                self._secondCoderParams.coder,
                '',
                self.noiseStart,
                self.noiseEnd
        )

    def start_first_single_test(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_first_coder_thread_class()
            self._firstThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._firstThreadClass.start()
        except:
            pass

    def start_first_test_cycle(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_first_coder_thread_class()
            self._firstThreadClass.set_auto(True)
            self._firstThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._firstThreadClass.autoStepFinished.connect(self._autoProgress.setValue)
            self._firstThreadClass.start()
        except:
            pass

    def start_cascade_single_test(self):
        self._firstCoderParams.create_coder()
        self._secondCoderParams.create_coder()
        try:
            self.set_cascade_coder_thread_class()
            self._cascadeThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._cascadeThreadClass.start()
        except:
            pass

    def start_cascade_test_cycle(self):
        self._firstCoderParams.create_coder()
        try:
            self.set_cascade_coder_thread_class()
            self._cascadeThreadClass.set_auto(True)
            self._cascadeThreadClass.stepFinished.connect(self._singleProgress.setValue)
            self._cascadeThreadClass.autoStepFinished.connect(self._autoProgress.setValue)
            self._cascadeThreadClass.start()
        except:
            pass
