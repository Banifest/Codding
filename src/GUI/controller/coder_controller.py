# coding=utf-8
from PyQt5.QtWidgets import QMessageBox

from src.coders.abstract_coder import AbstractCoder
from src.coders.casts import str_list_to_list
from src.coders.convolutional.coder import Coder as Convolutional
from src.coders.cyclical.coder import Coder as Cyclical
from src.coders.fountain.luby_transform import Coder as LubyTransform
from src.coders.linear.hamming import Coder as Hamming
from statistics.db.enum_coders_type import EnumCodersType


class CoderController:
    _coder_type: int = 0
    coder: AbstractCoder

    _hemSizePack: int = 120

    _cycSizePack: int = 120
    _cycPoly: int = 13

    _conListPoly: str = [3, 5, 7]
    _conCountReg: int = 3

    _fouSizePack: int = 30
    _fouSizeBlock: int = 10
    _fouCountBlock: int = 10

    _interleaver: int = 0

    def __init__(self):
        pass

    def set_coder_type(self, value: int) -> None:
        self._coder_type = value

    def set_hem_size_pack(self, value: int) -> None:
        self._hemSizePack = value

    def set_cyc_size_pack(self, value: int) -> None:
        self._cycSizePack = value

    def set_cyc_poly(self, value: int) -> None:
        self._cycPoly = value

    def set_con_list_poly(self, value: str) -> None:
        self._conListPoly = value

    def set_con_count_reg(self, value: int) -> None:
        self._conCountReg = value

    def set_fou_size_pack(self, value: int) -> None:
        self._fouSizePack = value

    def set_fou_size_block(self, value: int) -> None:
        self._fouSizeBlock = value

    def set_fou_count_block(self, value: int) -> None:
        self._fouCountBlock = value

    def set_interleaver(self, value: int) -> None:
        self._interleaver = value

    def create_coder(self):
        try:
            if self._coder_type == EnumCodersType.HAMMING.value:
                self.coder = Hamming(self._hemSizePack)
            elif self._coder_type == EnumCodersType.CYCLICAL.value:
                self.coder = Cyclical(
                        int(self._cycSizePack),
                        int(self._cycPoly)
                )
            elif self._coder_type == EnumCodersType.CONVOLUTION.value:
                self.coder = Convolutional(
                    str_list_to_list(self._conListPoly),
                        1,
                    int(len(str_list_to_list(self._conListPoly))),
                        self._conCountReg
                )
            elif self._coder_type == EnumCodersType.FOUNTAIN.value:
                self.coder = LubyTransform(
                        int(self._fouSizeBlock),
                        int(self._fouCountBlock),
                        int(self._fouSizePack)
                )
            # elif self._coder_type == 'Рида-Маллера':
            #     self.currentCoder = ReedMullerCoder(
            #             int(self._addCoderWindow.sizePackageTextBox.text()),
            #             int(self._addCoderWindow.powerReedMullerTextBox.text())
            #     )
            # elif self._coder_type == 'Сверточный для пакетов':
            #     self.currentCoder = ConvolutionalCoderForPacket(
            #             str_list_to_list(self._addCoderWindow.listPolynomialTextBox.text()),
            #             1,
            #             int(len(str_list_to_list(self._addCoderWindow.listPolynomialTextBox.text()))),
            #             int(self._addCoderWindow.countMemoryRegistersTextBox.text()),
            #             int(self._addCoderWindow.sizePackageTextBox.text())
            #     )
        except:
            QMessageBox().warning(
                None,
                "Поля заполнены не верной информацией",
                "Поля заполнены не верной информацией",
                QMessageBox.Ok
            )
