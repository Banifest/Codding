# coding=utf-8


def setup_main_window_noise(controller, window):
    window.packageErrorModeRadio.toggled.connect(controller.testParams.set_noise_mode)
    window.packageErrorModeRadio.toggled.emit(window.packageErrorModeRadio.isChecked())

    window.pakcageLengthSpinBox.valueChanged.connect(controller.testParams.set_noise_package_length)
    window.pakcageLengthSpinBox.valueChanged.emit(window.pakcageLengthSpinBox.value())

    window.isSplitPackageCheckBox.toggled.connect(controller.testParams.set_is_split_package)
    window.isSplitPackageCheckBox.toggled.emit(window.isSplitPackageCheckBox.isChecked())

    window.noiseStartEdit.valueChanged.connect(controller.testParams.set_noise_start)
    window.noiseStartEdit.valueChanged.emit(window.noiseStartEdit.value())
    window.noiseFinishEdit.valueChanged.connect(controller.testParams.set_noise_end)
    window.noiseFinishEdit.valueChanged.emit(window.noiseFinishEdit.value())
