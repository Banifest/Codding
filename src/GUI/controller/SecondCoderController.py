class SecondCoderController:
    _hemSizePack2: int = 120

    _cycSizePack2: int = 120
    _cycPoly2: int = 13

    _conListPoly2: list = [3, 5, 7]
    _conCountReg2: int = 3

    _fouSizePack2: int = 30
    _fouSizeBlock2: int = 10
    _fouCountBlock2: int = 10

    _interleaver2: int = 0

    def set_hem_size_pack2(self, value: int) -> None:
        self._hemSizePack2 = value

    def set_cyc_size_pack2(self, value: int) -> None:
        self._cycSizePack2 = value

    def set_cyc_poly2(self, value: int) -> None:
        self._cycPoly2 = value

    def set_con_list_poly2(self, value: str) -> None:
        self._conListPoly2 = value

    def set_con_count_reg2(self, value: int) -> None:
        self._conCountReg2 = value

    def set_fou_size_pack2(self, value: int) -> None:
        self._fouSizePack2 = value

    def set_fou_size_block2(self, value: int) -> None:
        self._fouSizeBlock2 = value

    def set_fou_count_block2(self, value: int) -> None:
        self._fouCountBlock2 = value

    def set_interleaver2(self, value: int) -> None:
        self._interleaver2 = value
