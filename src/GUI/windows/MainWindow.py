from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

# noinspection PyUnresolvedReferences
import resources.img_rc
from src.logger import log


class MainWindow(QMainWindow):
    def __init__(self, controller):
        log.debug("Создание главного окна")

        super(MainWindow, self).__init__()
        self.controller = controller
        uic.loadUi(r'.\src\GUI\UI\window.ui', self)

        self.sizePackHemEdit.valueChanged.connect(self.controller.firstCoderParams.set_hem_size_pack)

        self.sizePackCycEdit.valueChanged.connect(self.controller.firstCoderParams.set_cyc_size_pack)
        self.poliCycEdit.valueChanged.connect(self.controller.firstCoderParams.set_cyc_poly)

        self.listConvEdit.textChanged.connect(self.controller.firstCoderParams.set_con_list_poly)
        self.countRegConvEdit.valueChanged.connect(self.controller.firstCoderParams.set_con_count_reg)

        self.sizePackFounEdit.valueChanged.connect(self.controller.firstCoderParams.set_fou_size_pack)
        self.sizeBlockFounEdit.valueChanged.connect(self.controller.firstCoderParams.set_fou_size_block)
        self.countBlockFounEdit.valueChanged.connect(self.controller.firstCoderParams.set_fou_count_block)

        self.lenFirstInterEdit.valueChanged.connect(self.controller.firstCoderParams.set_interleaver)
        self.interFirstCheckBox.stateChanged.connect(
                lambda val: self.lenFirstInterEdit.setEnabled(self.lenFirstInterEdit.isEnabled() ^ 1)
        )

        self.firstCoderSetting.currentChanged.connect(self.controller.firstCoderParams.set_coder_type)

        # Second coder description
        self.sizePackHemEdit2.valueChanged.connect(self.controller.secondCoderParams.set_hem_size_pack)

        self.sizePackCycEdit2.valueChanged.connect(self.controller.secondCoderParams.set_cyc_size_pack)
        self.poliCycEdit2.valueChanged.connect(self.controller.secondCoderParams.set_cyc_poly)

        self.listConvEdit2.textChanged.connect(self.controller.secondCoderParams.set_con_list_poly)
        self.countRegConvEdit2.valueChanged.connect(self.controller.secondCoderParams.set_con_count_reg)

        self.sizePackFounEdit2.valueChanged.connect(self.controller.secondCoderParams.set_fou_size_pack)
        self.sizeBlockFounEdit2.valueChanged.connect(self.controller.secondCoderParams.set_fou_size_block)
        self.countBlockFounEdit2.valueChanged.connect(self.controller.secondCoderParams.set_fou_count_block)

        self.interSecondCheckBox.stateChanged.connect(
                lambda val: self.lenSecondInterEdit.setEnabled(self.lenSecondInterEdit.isEnabled() ^ 1)
        )
        self.lenSecondInterEdit.valueChanged.connect(self.controller.secondCoderParams.set_interleaver)

        self.secondCoderSetting.currentChanged.connect(self.controller.secondCoderParams.set_coder_type)

        # self.action_import_from_json.triggered.connect(self.controller.import_from_json)

        self.noiseStartEdit.valueChanged.connect(self.controller.testParams.set_noise_start)
        self.noiseFinishEdit.valueChanged.connect(self.controller.testParams.set_noise_end)
        self.countTestEdit.valueChanged.connect(self.controller.testParams.set_count_test)
        self.informationEdit.textChanged.connect(self.controller.testParams.set_test_info)

        self.controller.testParams.set_single_progress(self.singleProgress)
        self.controller.testParams.set_auto_progress(self.autoProgress)

        self.startSingleFirstCoderButton.clicked.connect(self.controller.testParams.start_first_single_test)
        self.startTestsFirstCoderButton.clicked.connect(self.controller.testParams.start_first_test_cycle)
        self.show()