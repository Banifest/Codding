# coding=utf-8
from abc import ABC
from typing import Optional

from src.coders.abstract_coder import AbstractCoder
from src.coders.casts import str_list_to_list
from src.coders.convolutional.coder import Coder as Convolutional
from src.coders.cyclical.coder import Coder as Cyclical
from src.coders.fountain.luby_transform import Coder as LubyTransform
from src.coders.linear.hamming import Coder as Hamming
from src.statistics.db.enum_coders_type import EnumCodersType


class GeneralCoderSimulate(ABC):
    coder: AbstractCoder
    _coderTypeInt: int
    _coderType: EnumCodersType

    _hemSizePack: int

    _cycSizePack: int
    _cycPoly: int

    _conListPoly: str
    _conCountReg: int

    _fouSizePack: int
    _fouSizeBlock: int
    _fouCountBlock: int

    def __init__(
            self,
            coder_type_int: Optional[int] = None,
            coder_type: Optional[EnumCodersType] = None,
            hem_size_pack: Optional[int] = None,
            cyc_size_pack: Optional[int] = None,
            cyc_poly: Optional[int] = None,
            con_list_poly: Optional[str] = None,
            con_count_reg: Optional[int] = None,
            fou_size_pack: Optional[int] = None,
            fou_size_block: Optional[int] = None,
            fou_count_block: Optional[int] = None
    ):
        self._coderTypeInt = coder_type_int
        self._coderType = coder_type

        if coder_type is not None:
            self._coderTypeInt = coder_type.value

        self._hemSizePack = hem_size_pack
        self._cycSizePack = cyc_size_pack
        self._cycPoly = cyc_poly
        self._conListPoly = con_list_poly
        self._conCountReg = con_count_reg
        self._fouSizePack = fou_size_pack
        self._fouSizeBlock = fou_size_block
        self._fouCountBlock = fou_count_block

    def create_coder(self) -> AbstractCoder:
        if self._coderTypeInt == EnumCodersType.HAMMING.value:
            self.coder = Hamming(self._hemSizePack)
        elif self._coderTypeInt == EnumCodersType.CYCLICAL.value:
            self.coder = Cyclical(
                information_length=int(self._cycSizePack),
                polynomial=int(self._cycPoly)
            )
        elif self._coderTypeInt == EnumCodersType.CONVOLUTION.value:
            self.coder = Convolutional(
                str_list_to_list(self._conListPoly),
                1,  # TODO change to constant or remove
                int(len(str_list_to_list(self._conListPoly))),
                self._conCountReg
            )
        elif self._coderTypeInt == EnumCodersType.FOUNTAIN.value:
            self.coder = LubyTransform(
                int(self._fouSizeBlock),
                int(self._fouCountBlock),
                int(self._fouSizePack)
            )
        return self.coder
