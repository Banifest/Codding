# coding=utf-8
from typing import Optional, Union, List

from src.channel import chanel
from src.channel.enum_bit_transfer_result import EnumBitTransferResult
from src.channel.enum_noise_mode import EnumNoiseMode
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders.abstract_coder import AbstractCoder
from src.coders.interleaver import Interleaver
from src.helper.error.exception.codding_exception import CodingException
from src.helper.error.exception.parameters_parse_exception import ParametersParseException
from src.logger import log


class Codec:
    noiseProbability: int = 0
    _countCyclical: int = 1
    # Information about transfer on chanel
    _information: str = ""
    _coder: AbstractCoder
    _interleaver: Interleaver.Interleaver = False

    # Package noise mode attr
    _noiseMode: EnumNoiseMode
    _noisePackageLength: int

    class TransferStatistic:
        result_status: EnumPackageTransferResult = EnumPackageTransferResult.SUCCESS
        quantity_successful_bits: int = 0
        quantity_error_bits: int = 0
        quantity_repair_bits: int = 0
        quantity_shadow_bits: int = 0
        quantity_changed_bits: int = 0
        based_error_bits: int = 0
        based_correct_bits: int = 0
        current_information_state: list = []

    def __init__(
            self,
            coder: Optional[AbstractCoder],
            noise_probability: Union[int, float],
            count_cyclical: Optional[int],
            duplex: Optional[bool],
            interleaver: Optional[Interleaver.Interleaver],
            noise_mode: EnumNoiseMode,
            noise_package_length: int,
            noise_package_period: int,
    ):

        log.debug("Create chanel")
        self._noiseMode = noise_mode
        self._noisePackageLength = noise_package_length
        self._noisePackagePeriod = noise_package_period

        self._coder: AbstractCoder = coder
        if noise_probability is not None:
            self.noiseProbability = noise_probability
        if count_cyclical is not None:
            self._countCyclical = count_cyclical
        if duplex is not None:
            self.duplex = duplex
        if interleaver is not None:
            self._interleaver = interleaver
        log.debug("Chanel created")

    def __str__(self) -> str:
        return \
            "Вероятность ошибки в канале - {0}.\n" \
            "Является ли канал двухсторонним - {1}.\n" \
            "Используеммый кодер:\n {2}." \
            "Используется ли перемежитель на данном канале связи - {3}.\n" \
            "Количество циклов передачи Package - {4}\n" \
            "Информация о последней передаче:\n{5}".format(
                self.noiseProbability,
                "Да" if self.duplex else "Нет",
                str(self._coder),
                "Да" if self._interleaver else "Нет",
                self._countCyclical,
                self._information
            )

    def transfer_one_step(self, information: List[int]) -> TransferStatistic:
        transfer_statistic = Codec.TransferStatistic()

        #  Разбиение на Package
        if self._coder.isDivIntoPackage:
            block_list = chanel.Chanel().divide_on_blocks(
                information=information,
                block_len=self._coder.lengthInformation
            )
        else:
            block_list = [information.copy()]

        for block in block_list:
            current_information: List[int] = block.copy()
            log.info("Transfer bits - {0}".format(current_information))
            status: EnumBitTransferResult = EnumBitTransferResult.SUCCESS
            normalization_information: List[int] = self._coder.try_normalization(current_information)
            try:
                current_information = self._coder.encoding(normalization_information)

                if self._interleaver:
                    current_information = self._interleaver.shuffle(current_information)

                help_information = current_information

                compare_information: list = current_information
                current_information = self._do_noise(
                    information=current_information,
                    noise_probability=self.noiseProbability,
                )
                transfer_statistic.based_correct_bits, transfer_statistic.based_error_bits = self._get_change_state(
                    source_state=compare_information,
                    current_state=current_information
                )

                if help_information != current_information:
                    status = EnumBitTransferResult.REPAIR

                if self._interleaver:
                    current_information = self._interleaver.reestablish(current_information)

                current_information = self._coder.decoding(current_information)
            except CodingException:
                status = EnumBitTransferResult.ERROR
                log.info(
                    "During decoding package {0} founded cannot repair error".format(current_information))
                self._information = "Package corrupted amd cannot be rapair\n"
            else:
                if current_information == normalization_information:
                    if status != EnumBitTransferResult.REPAIR:
                        status = EnumBitTransferResult.SUCCESS
                    log.info("Package {0} transferred successfully".format(information))
                    self._information = "Package transferred successfully\n"
                else:
                    status = EnumBitTransferResult.SHADOW
                    log.error("Package {0} corrupted and impossible to repair it".format(
                        current_information))
                    self._information = "Package {0} corrupted and impossible to repair it\n"

            current_step_success_bits = self._get_different_information(current_information, normalization_information)
            transfer_statistic.quantity_successful_bits += current_step_success_bits
            transfer_statistic.quantity_error_bits += len(normalization_information) - current_step_success_bits

            if status == EnumBitTransferResult.ERROR:
                transfer_statistic.result_status = EnumPackageTransferResult.ERROR
            elif status == EnumBitTransferResult.SHADOW:
                transfer_statistic.result_status = EnumPackageTransferResult.SHADOW
            elif status == EnumBitTransferResult.REPAIR \
                    and transfer_statistic.result_status != EnumPackageTransferResult.ERROR \
                    and transfer_statistic.result_status != EnumPackageTransferResult.SHADOW:
                transfer_statistic.result_status = EnumPackageTransferResult.REPAIR
            else:
                transfer_statistic.result_status = EnumPackageTransferResult.SUCCESS
        return transfer_statistic

    def get_transfer_one_step(self, information: List[int]) -> TransferStatistic:
        transfer_statistic = Codec.TransferStatistic()
        current_information_state: List[int] = information.copy()

        log.info("Transfer package - {0}".format(current_information_state))
        normalization_information: List[int] = self._coder.try_normalization(current_information_state)
        try:
            current_information_state = self._coder.encoding(normalization_information)

            if self._interleaver:
                current_information_state = self._interleaver.shuffle(current_information_state)

            compare_information: list = current_information_state
            current_information_state = self._do_noise(
                information=current_information_state,
                noise_probability=self.noiseProbability,
            )
            transfer_statistic.based_correct_bits, transfer_statistic.based_error_bits = self._get_change_state(
                source_state=compare_information,
                current_state=current_information_state
            )

            if self._interleaver:
                current_information_state = self._interleaver.reestablish(current_information_state)

            current_information_state = self._coder.decoding(current_information_state)
        except CodingException:
            log.info(
                "В ходе декодирования Packageа {0} была обнаружена неисправляемая ошибка".format(
                    current_information_state))
            self._information = "Package при передаче был повреждён и не подлежит востановлению\n"
        except:
            # TODO the same that and method below
            log.info(
                "В ходе декодирования Packageа {0} была обнаружена неисправляемая ошибка".format(
                    current_information_state))
            self._information = "Package при передаче был повреждён и не подлежит востановлению\n"
        else:
            if current_information_state == normalization_information:
                log.info("Package {0} был успешно передан".format(information))
                self._information = "Package был успешно передан\n"
            else:
                log.error("Package {0} был повреждён при передаче передан и ошибку не удалось обнаружить".format(
                    current_information_state))
                self._information = "Package при передаче был повреждён и не подлежит " \
                                    "востановлению\n"

        # Calculate count decoded bits
        current_step_success_bits = self._get_different_information(
            current_information_state, normalization_information)

        transfer_statistic.quantity_successful_bits += current_step_success_bits
        transfer_statistic.quantity_error_bits += len(normalization_information) - current_step_success_bits
        transfer_statistic.current_information_state = current_information_state
        return transfer_statistic

    def _do_noise(self, information: list, noise_probability: float) -> list:
        if self._noiseMode == EnumNoiseMode.SINGLE:
            return chanel.Chanel().gen_interference(information=information, straight=noise_probability)
        elif self._noiseMode == EnumNoiseMode.PACKAGE:
            return chanel.Chanel().generate_package_interference(
                information=information,
                length_of_block=self._noisePackageLength,
                frequency_of_block=self._noisePackagePeriod
            )
        elif self._noiseMode == EnumNoiseMode.MIX:
            single_package: list = chanel.Chanel().generate_package_interference(
                information=information,
                length_of_block=self._noisePackageLength,
                frequency_of_block=self._noisePackagePeriod
            )
            return chanel.Chanel().generate_package_interference(
                information=single_package,
                length_of_block=self._noisePackageLength,
                frequency_of_block=self._noisePackagePeriod
            )
        else:
            raise ParametersParseException(
                message=ParametersParseException.NOISE_MODE_UNDEFINED.message,
                long_message=ParametersParseException.NOISE_MODE_UNDEFINED.long_message
            )

    # noinspection PyMethodMayBeStatic
    def _get_change_state(
            self,
            source_state: List[int],
            current_state: List[int]
    ) -> List[int]:
        correct_bits: int = 0
        error_bits: int = 0

        if len(source_state) != len(current_state):
            raise CodingException(
                message=CodingException.LENGTH_OF_CURRENT_SOURCE_STATE_DIFF.message,
                long_message=CodingException.LENGTH_OF_CURRENT_SOURCE_STATE_DIFF.long_message,
                additional_information=[len(current_state), len(source_state)]
            )

        for iterator in range(len(source_state)):
            if source_state[iterator] == current_state[iterator]:
                correct_bits += 1
            else:
                error_bits += 1

        return [correct_bits, error_bits]

    def _get_different_information(self, first_info: List[int], second_info: List[int]) -> int:
        distance = sum([1 if first_info[x] == second_info[x] else 0 for x in
                        range(min(len(first_info), len(second_info)))])
        distance += abs(len(first_info) - len(second_info))
        return distance
