from PyQt5 import uic
from PyQt5.QtWidgets import QCheckBox, QLabel, QLineEdit, QProgressBar, QPushButton, QWidget

from src.channel.cascade import Cascade
from src.channel.channel import Channel
from src.logger import log


class TestCascadeCoderWindow(QWidget):
    channel: Channel
    cascade: Cascade

    noiseProbabilityTextBox: QLineEdit
    countCyclicalTextBox: QLineEdit
    informationTextBox: QLineEdit
    lengthSmashingTextBox: QLineEdit
    duplexCheckBox: QCheckBox
    interleaverCheckBox: QCheckBox

    interleaverLabelSecond: QLabel
    lengthSmashingLabelSecond: QLabel

    testingProgressBar: QProgressBar
    autoTestingProgressBar: QProgressBar

    submitButton: QPushButton
    lastResultButton: QPushButton
    autoTestButton: QPushButton

    lastResult: str = ""

    def __init__(self, controller):
        log.debug("Создание окна тестирования кодера")
        super().__init__()

        uic.loadUi(r'src\GUI\UI\test_cascade_coder.ui', self)
        self.controller = controller
        self.controller._testCoderWindow = self

        self.begin_test_button.clicked.connect(lambda: self.controller.starting_test(False))
        self.begin_auto_test_button.clicked.connect(lambda: self.controller.starting_test(True))
        self.get_last_result_button.clicked.connect(self.controller.get_last_result)

        self.is_interleaver_first.stateChanged.connect(lambda val: self.first_length_text_box.setEnabled
        (self.first_length_text_box.isEnabled() ^ 1))
        self.is_interleaver_second.stateChanged.connect(lambda val: self.second_length_text_box.setEnabled
        (self.second_length_text_box.isEnabled() ^ 1))

        self.show()
