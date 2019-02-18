# coding=utf-8


def setup_main_window_noise(controller, window):
    window.singleErrorModeRadio.toggled.connect(controller.testParams.set_noise_mode)
    window.singleErrorModeRadio.toggled.emit(window.singleErrorModeRadio.isChecked())

    window.pakcageLengthSpinBox.valueChanged.connect(controller.testParams.set_noise_package_length)
    window.pakcageLengthSpinBox.valueChanged.emit(window.pakcageLengthSpinBox.value())

    window.isSplitPackageCheckBox.toggled.connect(controller.testParams.set_is_split_package)
    window.isSplitPackageCheckBox.toggled.emit(window.isSplitPackageCheckBox.isChecked())

    window.noiseStartEdit.valueChanged.connect(controller.testParams.set_noise_start)
    window.noiseStartEdit.valueChanged.emit(window.noiseStartEdit.value())
    window.noiseFinishEdit.valueChanged.connect(controller.testParams.set_noise_end)
    window.noiseFinishEdit.valueChanged.emit(window.noiseFinishEdit.value())

    window.countStepsInCycleEdit.valueChanged.connect(controller.testParams.set_quantity_steps_in_test_cycle)
    window.countStepsInCycleEdit.valueChanged.emit(window.countStepsInCycleEdit.value())
