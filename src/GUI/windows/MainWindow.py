from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

# noinspection PyUnresolvedReferences
import Resources.img_rc
from GUI.windows.AddCoderWindow import AddCoderWindow
# from GUI.windows.TestCascadeCoderWindow import TestCascadeCoderWindow
# from GUI.windows.TestCoderWindow import TestCoderWindow
from src.logger import log


class MainWindow(QMainWindow):
    def __init__(self, controller):
        log.debug("Создание главного окна")

        super(MainWindow, self).__init__()
        self.controller = controller
        uic.loadUi(r'src\GUI\UI\main_window.ui', self)

        self.action_create_new_coder.triggered.connect(self.controller.set_create_coder_window)
        self.action_test_simple_coder.triggered.connect(self.controller.set_test_coder_window)
        self.action_test_cascade_coder.triggered.connect(lambda: TestCascadeCoderWindow(self))
        self.action_about_coder.triggered.connect(lambda: AddCoderWindow(self))

        self.show()

    def closeEvent(self, *args, **kwargs):
        self.controller.del_add_coder_window()
        self.controller.del_test_simple_coder_window()
        self.controller.del_test_cascade_coder_window()
