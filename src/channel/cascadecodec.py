# coding=utf-8
# coding=utf-8
from typing import Optional

from src.channel import codec, chanel
from src.channel.codec import Codec
from src.channel.enum_noise_mode import EnumNoiseMode
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int
from src.coders.interleaver import Interleaver


class CascadeCodec(codec.Codec):
    firstCoder: abstract_coder.AbstractCoder
    firstInterleaver: Interleaver.Interleaver
    secondCoder: abstract_coder.AbstractCoder
    secondInterleaver: Interleaver.Interleaver = None
    # TODO выяснить что это? мб бить на пакеты или нет вообще хз. + добавить Enum
    mode: int = 0

    def __init__(
            self,
            first_coder: abstract_coder.AbstractCoder,
            second_coder: abstract_coder.AbstractCoder,
            noise_probability: int or float,
            count_cyclical: Optional[int],
            duplex: Optional[bool],
            first_interleaver: Optional[Interleaver.Interleaver],
            second_interleaver: Optional[Interleaver.Interleaver],
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            is_split_package: bool,
            mode: int = 0,
    ):
        super().__init__(
            None,
            noise_probability,
            count_cyclical,
            duplex,
            first_interleaver,
            noise_mode=noise_mode,
            noise_package_length=noise_package_length,
            is_split_package=is_split_package,
        )
        self.firstCoder = first_coder
        self.secondCoder = second_coder
        self.mode = mode

        self.firstInterleaver = first_interleaver if first_interleaver is not None else None
        self.secondInterleaver = second_interleaver if second_interleaver is not None else None

    def transfer_one_step(self, information: list) -> Codec.TransferStatistic:
        if self.mode == 0:
            #  Разделение на пакеты
            package_list = chanel.Chanel().divide_on_blocks(
                information=information,
                block_len=self.firstCoder.lengthInformation
            )

            transfer_information: Codec.TransferStatistic
            for x in package_list:
                self.coder = self.secondCoder
                normalization_information = self.firstCoder.try_normalization(x)

                current_information_state: list = self.firstCoder.encoding(normalization_information)

                if self.secondInterleaver is not None:
                    current_information_state = self.secondInterleaver.shuffle(current_information_state)

                transfer_information = self.get_transfer_one_step(current_information_state)

                # обрезка добавленных битов для нормализации
                current_information_state = transfer_information.current_information_state[
                                            -len(current_information_state):]

                if self.secondInterleaver is not None:
                    current_information_state = self.secondInterleaver.reestablish(current_information_state)

                current_information_state = self.firstCoder.decoding(current_information_state)
                transfer_information.current_information_state = current_information_state
                if bit_list_to_int(current_information_state) != bit_list_to_int(normalization_information):
                    transfer_information.result_status = EnumPackageTransferResult.ERROR
                    return transfer_information

            transfer_information.result_status = EnumPackageTransferResult.REPAIR
            return transfer_information

        elif self.mode == 1:
            first_coder_information: list = self.firstCoder.encoding(information)
            if self.firstInterleaver is not None:
                first_coder_information = self.firstInterleaver.shuffle(first_coder_information)

            second_coder_information: list = self.firstCoder.encoding(information)
            if self.secondInterleaver is not None:
                second_coder_information = self.secondInterleaver.shuffle(second_coder_information)

                transfer_information = self._do_noise(information=first_coder_information + second_coder_information,
                                                      noise_probability=self.noiseProbability)

            if self.firstInterleaver is not None:
                first_coder_information = self.firstInterleaver.reestablish(first_coder_information)

            if self.secondInterleaver is not None:
                second_coder_information = self.secondInterleaver.reestablish(second_coder_information)

            first_coder_information = self.firstCoder.decoding(first_coder_information)
            second_coder_information = self.secondCoder.decoding(second_coder_information)
            if bit_list_to_int(first_coder_information) != bit_list_to_int(first_coder_information) \
                    and bit_list_to_int(second_coder_information) != bit_list_to_int(second_coder_information):
                return [EnumPackageTransferResult.ERROR, transfer_information[1], transfer_information[2],
                        transfer_information[3], transfer_information[4]]
            else:
                return [EnumPackageTransferResult.REPAIR, transfer_information[1], transfer_information[2],
                        transfer_information[3], transfer_information[4]]
