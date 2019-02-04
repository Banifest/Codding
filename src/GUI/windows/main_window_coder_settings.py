# coding=utf-8


def setup_main_window_coder_settings(controller, window):
    window.packageErrorModeRadio.toggled.connect(controller.testParams.set_noise_mode)
    window.packageErrorModeRadio.toggled.emit(window.singleErrorModeRadio.isEnabled())

    window.pakcageLengthSpinBox.valueChanged.connect(controller.testParams.set_noise_package_length)
    window.pakcageLengthSpinBox.valueChanged.emit(window.pakcageLengthSpinBox.value())

    window.isSplitPackageCheckBox.toggled.connect(controller.testParams.set_is_split_package)
    window.isSplitPackageCheckBox.toggled.emit(window.isSplitPackageCheckBox.isChecked())
