from PyQt5 import uic
from PyQt5.QtWidgets import QGridLayout, QWidget

from src.logger import log


class TestCoderWindow(QWidget):
    def __init__(self, controller):
        self.grid = QGridLayout()
        log.debug("Создание окна тестирования кодера")
        super().__init__()
        self.controller = controller
        uic.loadUi(r'.\src\GUI\UI\test_simple_coder.ui', self)

        self.controller.set_window(self)
        self.begin_test_button.clicked.connect(lambda: self.controller.starting_test(False))
        self.begin_auto_test_button.clicked.connect(lambda: self.controller.starting_test(True))
        self.get_last_result_button.clicked.connect(self.controller.get_last_result)

        self.noise_start.valueChanged.connect(self.controller.set_start)
        self.noise_finish.valueChanged.connect(self.controller.set_finish)

        self.is_interleaver_first.stateChanged.connect(
                lambda val: self.first_length_text_box.setEnabled(self.first_length_text_box.isEnabled() ^ 1)
                )

        self.show()
