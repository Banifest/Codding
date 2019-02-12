# coding=utf-8


def setup_main_window_coder(controller, window):
    window.firstCoderSetting.currentChanged.connect(controller.firstCoderParams.set_coder_type)
    window.firstCoderSetting.currentChanged.emit(window.firstCoderSetting.currentIndex())

    window.sizePackHemEdit.valueChanged.connect(controller.firstCoderParams.set_hem_size_pack)
    window.sizePackHemEdit.valueChanged.emit(window.sizePackHemEdit.value())

    window.sizePackCycEdit.valueChanged.connect(controller.firstCoderParams.set_cyc_size_pack)
    window.sizePackCycEdit.valueChanged.emit(window.sizePackCycEdit.value())

    window.poliCycEdit.valueChanged.connect(controller.firstCoderParams.set_cyc_poly)
    window.poliCycEdit.valueChanged.emit(window.poliCycEdit.value())

    window.listConvEdit.textChanged.connect(controller.firstCoderParams.set_con_list_poly)
    window.listConvEdit.textChanged.emit(window.listConvEdit.text())
    window.countRegConvEdit.valueChanged.connect(controller.firstCoderParams.set_con_count_reg)
    window.countRegConvEdit.valueChanged.emit(window.countRegConvEdit.value())

    window.sizePackFounEdit.valueChanged.connect(controller.firstCoderParams.set_fou_size_pack)
    window.sizePackFounEdit.valueChanged.emit(window.sizePackFounEdit.value())
    window.sizeBlockFounEdit.valueChanged.connect(controller.firstCoderParams.set_fou_size_block)
    window.sizeBlockFounEdit.valueChanged.emit(window.sizeBlockFounEdit.value())
    window.countBlockFounEdit.valueChanged.connect(controller.firstCoderParams.set_fou_count_block)
    window.countBlockFounEdit.valueChanged.emit(window.countBlockFounEdit.value())

    # Interleaver
    window.lenFirstInterEdit.valueChanged.connect(controller.testParams.set_length_first_interleaver)
    window.lenFirstInterEdit.valueChanged.emit(window.lenFirstInterEdit.value())

    window.interFirstCheckBox.toggled.connect(controller.testParams.set_flg_first_interleaver)
    window.interFirstCheckBox.toggled.emit(window.interFirstCheckBox.isChecked())


def setup_main_window_second_coder(controller, window):
    window.secondCoderSetting.currentChanged.connect(controller.secondCoderParams.set_coder_type)
    window.secondCoderSetting.currentChanged.emit(window.secondCoderSetting.currentIndex())

    window.sizePackHemEdit2.valueChanged.connect(controller.secondCoderParams.set_hem_size_pack)
    window.sizePackHemEdit2.valueChanged.emit(window.sizePackHemEdit2.value())

    window.sizePackCycEdit2.valueChanged.connect(controller.secondCoderParams.set_cyc_size_pack)
    window.sizePackCycEdit2.valueChanged.emit(window.sizePackCycEdit2.value())

    window.poliCycEdit2.valueChanged.connect(controller.secondCoderParams.set_cyc_poly)
    window.poliCycEdit2.valueChanged.emit(window.poliCycEdit2.value())

    window.listConvEdit2.textChanged.connect(controller.secondCoderParams.set_con_list_poly)
    window.listConvEdit2.textChanged.emit(window.listConvEdit2.text())
    window.countRegConvEdit2.valueChanged.connect(controller.secondCoderParams.set_con_count_reg)
    window.countRegConvEdit2.valueChanged.emit(window.countRegConvEdit2.value())

    window.sizePackFounEdit2.valueChanged.connect(controller.secondCoderParams.set_fou_size_pack)
    window.sizePackFounEdit2.valueChanged.emit(window.sizePackFounEdit2.value())
    window.sizeBlockFounEdit2.valueChanged.connect(controller.secondCoderParams.set_fou_size_block)
    window.sizeBlockFounEdit2.valueChanged.emit(window.sizeBlockFounEdit2.value())
    window.countBlockFounEdit2.valueChanged.connect(controller.secondCoderParams.set_fou_count_block)
    window.countBlockFounEdit2.valueChanged.emit(window.countBlockFounEdit2.value())

    # Interleaver
    window.lenSecondInterEdit.valueChanged.connect(controller.testParams.set_length_second_interleaver)
    window.lenSecondInterEdit.valueChanged.emit(window.lenSecondInterEdit.value())

    window.interSecondCheckBox.toggled.connect(controller.testParams.set_flg_second_interleaver)
    window.interSecondCheckBox.toggled.emit(window.interSecondCheckBox.isChecked())
