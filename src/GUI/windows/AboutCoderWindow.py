# coding=utf-8
# coding=utf-8
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class AboutCoderWindow(QDialog):
    def __init__(self, controller):
        super(AboutCoderWindow, self).__init__()
        self.controller = controller
        self.controller._dialogAboutCoder = self
        uic.loadUi(r'.\src\GUI\UI\about_coder_dialog.ui', self)

        self.first_coder_button.clicked.connect(self.controller.redraw_dialog_info)
        self.second_coder_button.clicked.connect(self.controller.redraw_dialog_info)
        self.controller.redraw_dialog_info()
        self.show()
