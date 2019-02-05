# coding=utf-8
# coding=utf-8
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from GUI.windows.main_window_coder_settings import setup_main_window_coder, setup_main_window_second_coder
from GUI.windows.main_window_noise import setup_main_window_noise
from src.GUI.globals_signals import globalSignals
from src.logger import log


class MainWindow(QMainWindow):
    def __init__(self, controller):
        log.debug("Создание главного окна")

        super(MainWindow, self).__init__()
        self.controller = controller
        uic.loadUi(r'.\src\GUI\UI\window.ui', self)

        setup_main_window_coder(controller, self)
        setup_main_window_second_coder(controller, self)

        self.countTestEdit.valueChanged.connect(self.controller.testParams.set_count_test)
        self.informationEdit.textChanged.connect(self.controller.testParams.set_test_info)
        self.cascadeModeComboBox.activated[str].connect(self.controller.testParams.set_mode_cascade)

        globalSignals.stepFinished.connect(self.singleProgress.setValue)
        globalSignals.autoStepFinished.connect(self.autoProgress.setValue)

        self.startSingleFirstCoderButton.clicked.connect(self.controller.testParams.start_first_single_test)
        self.startTestsFirstCoderButton.clicked.connect(self.controller.testParams.start_first_test_cycle)
        self.startSingleCascadeCoderButton.clicked.connect(self.controller.testParams.start_cascade_single_test)
        self.startTestsCascadeCoderButton.clicked.connect(self.controller.testParams.start_cascade_test_cycle)

        setup_main_window_noise(controller=controller, window=self)
        self.show()
