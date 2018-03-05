class FirstCoderController:
    _hemSizePack: int = 120

    _cycSizePack: int = 120
    _cycPoly: int = 13

    _conListPoly: list = [3, 5, 7]
    _conCountReg: int = 3

    _fouSizePack: int = 30
    _fouSizeBlock: int = 10
    _fouCountBlock: int = 10

    _interleaver: int = 0

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
