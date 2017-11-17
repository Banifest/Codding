from GUI.windows.AboutCoderWindow import AboutCoderWindow


class AboutCoderController:
    _dialogAboutCoder: AboutCoderWindow

    def __init__(self, _mainController):
        self._mainController = _mainController

    def redraw_dialog_info(self):
        if self._dialogAboutCoder.first_coder_button.isChecked():
            if self._mainController.firstCoderForCascade is None:
                self._dialogAboutCoder.coder_name_label.setText("Нет кодера")
                self._dialogAboutCoder.length_information_label.setText("Нет кодера")
                self._dialogAboutCoder.coder_speed_label.setText("Нет кодера")
                self._dialogAboutCoder.length_coding_word_label.setText("Нет кодера")
            else:
                self._dialogAboutCoder.coder_name_label.setText(self._mainController.firstCoderForCascade.name)
                self._dialogAboutCoder.length_information_label.setText(
                    str(self._mainController.firstCoderForCascade.lengthInformation))
                self._dialogAboutCoder.coder_speed_label.setText(
                    str(self._mainController.firstCoderForCascade.get_speed()))
                self._dialogAboutCoder.length_coding_word_label.setText(
                        str(self._mainController.firstCoderForCascade.lengthTotal))
        else:
            if self._dialogAboutCoder.second_coder_button.isChecked():
                if self._mainController.secondCoderForCascade is None:
                    self._dialogAboutCoder.coder_name_label.setText("Нет кодера")
                    self._dialogAboutCoder.length_information_label.setText("Нет кодера")
                    self._dialogAboutCoder.coder_speed_label.setText("Нет кодера")
                    self._dialogAboutCoder.length_coding_word_label.setText("Нет кодера")
                else:
                    self._dialogAboutCoder.coder_name_label.setText(self._mainController.secondCoderForCascade.name)
                    self._dialogAboutCoder.length_information_label.setText(
                        str(self._mainController.secondCoderForCascade.lengthInformation))
                    self._dialogAboutCoder.coder_speed_label.setText(str(
                            self._mainController.secondCoderForCascade.get_speed()))
                    self._dialogAboutCoder.coder_speed_label.setText(str(
                            self._mainController.length_coding_word_label.lengthTotal))
