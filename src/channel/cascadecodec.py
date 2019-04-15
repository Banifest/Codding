# coding=utf-8
# coding=utf-8
from typing import Optional, Union

from src.channel import codec, chanel
from src.channel.codec import Codec
from src.channel.enum_noise_mode import EnumNoiseMode
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders import abstract_coder
from src.coders.casts import bit_list_to_int
from src.coders.interleaver import Interleaver


class CascadeCodec(codec.Codec):
    _firstCoder: abstract_coder.AbstractCoder
    _firstInterleaver: Interleaver.Interleaver
    _secondCoder: abstract_coder.AbstractCoder
    _secondInterleaver: Interleaver.Interleaver = None
    # TODO выяснить что это? мб бить на пакеты или нет вообще хз. + добавить Enum
    mode: int = 0

    def __init__(
            self,
            first_coder: abstract_coder.AbstractCoder,
            second_coder: abstract_coder.AbstractCoder,
            noise_probability: Union[int, float],
            count_cyclical: Optional[int],
            duplex: Optional[bool],
            first_interleaver: Optional[Interleaver.Interleaver],
            second_interleaver: Optional[Interleaver.Interleaver],
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            noise_package_period: int,
            mode: int = 0,
    ):
        super().__init__(
            coder=None,
            noise_probability=noise_probability,
            count_cyclical=count_cyclical,
            duplex=duplex,
            interleaver=first_interleaver,
            noise_mode=noise_mode,
            noise_package_length=noise_package_length,
            noise_package_period=noise_package_period,
        )
        self._firstCoder = first_coder
        self._secondCoder = second_coder
        self.mode = mode

        self._firstInterleaver = first_interleaver if first_interleaver is not None else None
        self._secondInterleaver = second_interleaver if second_interleaver is not None else None

    def transfer_one_step(self, information: list) -> Codec.TransferStatistic:
        if self.mode == 0:
            #  Разделение на пакеты
            package_list = [information]
            if self._firstCoder.is_div_into_package:
                package_list = chanel.Chanel().divide_on_blocks(
                    information=information,
                    block_len=self._firstCoder.lengthInformation,
                )

            transfer_information: Codec.TransferStatistic
            for x in package_list:
                self.coder = self._secondCoder
                normalization_information = self._firstCoder.try_normalization(x)

                current_information_state: list = self._firstCoder.encoding(normalization_information)

                if self._secondInterleaver is not None:
                    current_information_state = self._secondInterleaver.shuffle(current_information_state)

                transfer_information = self.get_transfer_one_step(current_information_state)

                # обрезка добавленных битов для нормализации
                current_information_state = transfer_information.current_information_state[
                                            -len(current_information_state):]

                if self._secondInterleaver is not None:
                    current_information_state = self._secondInterleaver.reestablish(current_information_state)

                current_information_state = self._firstCoder.decoding(current_information_state)
                transfer_information.current_information_state = current_information_state
                if bit_list_to_int(current_information_state) != bit_list_to_int(normalization_information):
                    transfer_information.result_status = EnumPackageTransferResult.ERROR
                    return transfer_information

            transfer_information.result_status = EnumPackageTransferResult.REPAIR
            return transfer_information

        elif self.mode == 1:
            # TODO разобраться для чего эта ветка
            pass
            # first_coder_information: list = self.firstCoder.encoding(information)
            # if self.firstInterleaver is not None:
            #     first_coder_information = self.firstInterleaver.shuffle(first_coder_information)
            #
            # second_coder_information: list = self.firstCoder.encoding(information)
            # if self.secondInterleaver is not None:
            #     second_coder_information = self.secondInterleaver.shuffle(second_coder_information)
            #
            # information_after_change = self._do_noise(information=first_coder_information + second_coder_information,
            #                                       noise_probability=self.noiseProbability)
            #
            # if self.firstInterleaver is not None:
            #     first_coder_information = self.firstInterleaver.reestablish(first_coder_information)
            #
            # if self.secondInterleaver is not None:
            #     second_coder_information = self.secondInterleaver.reestablish(second_coder_information)
            #
            # first_coder_information = self.firstCoder.decoding(first_coder_information)
            # second_coder_information = self.secondCoder.decoding(second_coder_information)
            # if bit_list_to_int(first_coder_information) != bit_list_to_int(first_coder_information) \
            #         and bit_list_to_int(second_coder_information) != bit_list_to_int(second_coder_information):
            #
            #     return [EnumPackageTransferResult.ERROR, transfer_information[1], transfer_information[2],
            #             transfer_information[3], transfer_information[4]]
            # else:
            #     return [EnumPackageTransferResult.REPAIR, transfer_information[1], transfer_information[2],
            #             transfer_information[3], transfer_information[4]]
