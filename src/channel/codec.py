# coding=utf-8
from typing import Optional, Union, List

from channel.enum_bit_transfer_result import EnumBitTransferResult
from src.channel import chanel
from src.channel.enum_package_transfer_result import EnumPackageTransferResult
from src.coders.abstract_coder import AbstractCoder
from src.coders.exeption import CodingException
from src.coders.interleaver import Interleaver
from src.logger import log


class Codec:
    # Вероятность ошибки
    noiseProbability: int = 0
    # Количество циклов
    countCyclical: int = 1
    duplex: bool = False
    # Информация о процессе передачи информации
    # TODO Пересмотреть и переделать концепт хранения информации о канале
    information: str = ""
    coder: AbstractCoder
    interleaver: Interleaver.Interleaver = False
    countSuccessfullyMessage: int

    def __init__(
            self,
            coder: Optional[AbstractCoder],
            noise_probability: Union[int, float],
            count_cyclical: Optional[int],
            duplex: Optional[bool],
            interleaver: Optional[Interleaver.Interleaver]
    ):

        log.debug("Создание канала связи")
        self.coder: AbstractCoder = coder
        if noise_probability is not None:
            self.noiseProbability = noise_probability
        if count_cyclical is not None:
            self.countCyclical = count_cyclical
        if duplex is not None:
            self.duplex = duplex
        if interleaver is not None:
            self.interleaver = interleaver
        log.debug("Канал создан")

    def __str__(self) -> str:
        return "Вероятность ошибки в канале - {0}.\n" \
               "Является ли канал двухсторонним - {1}.\n" \
               "Используеммый кодер:\n {2}." \
               "Используется ли перемежитель на данном канале связи - {3}.\n" \
               "Количество циклов передачи пакета - {4}\n" \
               "Информация о последней передаче:\n{5}".format(
            self.noiseProbability,
            "Да" if self.duplex else "Нет",
            str(self.coder),
            "Да" if self.interleaver else "Нет",
            self.countCyclical,
            self.information
        )

    def transfer(self, information: list) -> str:
        count_successfully: int = 0
        self.information += "Начата циклическая передача пакета ({0}).\n Количество передач {1}.\n". \
            format(information, self.countCyclical)

        for number_of_cycle in range(self.countCyclical):
            try:
                now_information: list = information
                now_information = self.coder.encoding(now_information)
                if self.interleaver:
                    now_information = self.interleaver.shuffle(now_information)

                now_information = chanel.Chanel().gen_interference(now_information)

                if self.interleaver:
                    now_information = self.interleaver.reestablish(now_information)

                now_information = self.coder.decoding(now_information)
            except CodingException as err:
                self.information += "Пакет при передаче попыткой под номером {0} был повреждён и не подлежит " \
                                    "востановлению\n".format(number_of_cycle)
            else:
                if now_information == information:
                    count_successfully += 1
                    self.information += "Пакет при передаче попыткой под номером {0} был успешно передан\n".format(
                        number_of_cycle)
                else:
                    self.information += "Пакет при передаче попыткой под номером {0} был повреждён и не подлежит " \
                                        "востановлению\n".format(number_of_cycle)

        self.information += "Циклическая передача пакета ({0}) завершена.\n" \
                            "Всего попыток передать пакет {1}.\n" \
                            "Количство успешно переданных пакетов {2}.\n" \
                            "Количество неудачно переданных пакетов {3}.\n". \
            format(information, self.countCyclical, count_successfully, self.countCyclical - count_successfully)

        return self.information

    def transfer_one_step(self, information: list) -> [EnumPackageTransferResult, int, int, int, int]:
        #  Разбиение на пакеты
        success_bits: int = 0
        drop_bits: int = 0
        repair_bits: int = 0
        change_bits: int = 0
        if self.coder.is_div_into_package:
            block_list = chanel.Chanel().divide_on_blocks(
                information=information,
                block_len=self.coder.lengthInformation
            )
        else:
            block_list = [information.copy()]

        package_status: EnumPackageTransferResult = EnumPackageTransferResult.SUCCESS
        for block in block_list:
            current_information: List[int] = block.copy()
            log.info("Производиться передача последовательности битов - {0}".format(current_information))
            status: int = EnumBitTransferResult.SUCCESS
            normalization_information: List[int] = self.coder.try_normalization(current_information)
            try:
                current_information = self.coder.encoding(normalization_information)

                if self.interleaver:
                    current_information = self.interleaver.shuffle(current_information)

                help_information = current_information

                current_information = chanel.Chanel().gen_interference(current_information, self.noiseProbability)

                if help_information != current_information:
                    status = EnumBitTransferResult.REPAIR

                if self.interleaver:
                    current_information = self.interleaver.reestablish(current_information)

                current_information = self.coder.decoding(current_information)
            except CodingException as rcx_coding:
                status = EnumBitTransferResult.ERROR
                log.info(
                    "В ходе декодирования пакета {0} была обнаружена неисправляемая ошибка".format(current_information))
                self.information = "Пакет при передаче был повреждён и не подлежит востановлению\n"
            except:
                status = EnumBitTransferResult.ERROR
                log.info(
                    "В ходе декодирования пакета {0} была обнаружена неисправляемая ошибка".format(current_information))
                self.information = "Пакет при передаче был повреждён и не подлежит востановлению\n"
            else:
                if current_information == normalization_information:
                    if status != EnumBitTransferResult.REPAIR:
                        status = EnumBitTransferResult.SUCCESS
                    log.info("Пакет {0} был успешно передан".format(information))
                    self.information = "Пакет был успешно передан\n"
                else:
                    status = EnumBitTransferResult.SHADOW
                    log.error("Пакет {0} был повреждён при передаче передан и ошибку не удалось обнаружить".format(
                        current_information))
                    self.information = "Пакет при передаче был повреждён и не подлежит " \
                                       "востановлению\n"
            current_step_success_bits = sum([1 if current_information[x] == normalization_information[x] else 0
                                             for x in range(len(current_information))])
            success_bits += current_step_success_bits
            drop_bits += len(normalization_information) - current_step_success_bits
            if status == EnumBitTransferResult.ERROR or status == EnumBitTransferResult.SHADOW:
                package_status = EnumPackageTransferResult.ERROR
            elif status == EnumBitTransferResult.REPAIR and package_status != EnumPackageTransferResult.ERROR:
                package_status = EnumPackageTransferResult.REPAIR
        return [package_status, success_bits, drop_bits, repair_bits, change_bits]

    def get_transfer_one_step(self, information: list) -> list:
        success_bits: int = 0
        drop_bits: int = 0
        repair_bits: int = 0
        change_bits: int = 0
        package_status: EnumPackageTransferResult = EnumPackageTransferResult.SUCCESS
        now_information: List[int] = information.copy()

        log.info("Производиться передача последовательности битов - {0}".format(now_information))
        status: int = EnumBitTransferResult.SUCCESS
        normalization_information: List[int] = self.coder.try_normalization(now_information)
        try:
            now_information = self.coder.encoding(normalization_information)

            if self.interleaver:
                now_information = self.interleaver.shuffle(now_information)

            help_information = now_information

            now_information = chanel.Chanel().gen_interference(now_information, self.noiseProbability)

            if help_information != now_information:
                status = EnumBitTransferResult.REPAIR

            if self.interleaver:
                now_information = self.interleaver.reestablish(now_information)

            now_information = self.coder.decoding(now_information)
        except CodingException as err:
            status = EnumBitTransferResult.ERROR
            log.info(
                "В ходе декодирования пакета {0} была обнаружена неисправляемая ошибка".format(now_information))
            self.information = "Пакет при передаче был повреждён и не подлежит востановлению\n"
        except:
            status = EnumBitTransferResult.ERROR
            log.info(
                "В ходе декодирования пакета {0} была обнаружена неисправляемая ошибка".format(now_information))
            self.information = "Пакет при передаче был повреждён и не подлежит востановлению\n"
        else:
            if now_information == normalization_information:
                if status != EnumBitTransferResult.REPAIR:
                    status = EnumBitTransferResult.SUCCESS
                log.info("Пакет {0} был успешно передан".format(information))
                self.information = "Пакет был успешно передан\n"
            else:
                status = EnumBitTransferResult.SHADOW
                log.error("Пакет {0} был повреждён при передаче передан и ошибку не удалось обнаружить".format(
                    now_information))
                self.information = "Пакет при передаче был повреждён и не подлежит " \
                                   "востановлению\n"
        current_step_success_bits = sum([1 if now_information[x] == normalization_information[x] else 0
                                         for x in range(len(now_information))])
        success_bits += current_step_success_bits
        drop_bits += len(normalization_information) - current_step_success_bits
        if status == EnumBitTransferResult.ERROR or status == EnumBitTransferResult.SHADOW:
            package_status = EnumPackageTransferResult.ERROR
        elif status == EnumBitTransferResult.REPAIR and package_status != EnumPackageTransferResult.ERROR:
            package_status = EnumPackageTransferResult.REPAIR
        return [now_information, success_bits, drop_bits, repair_bits, change_bits]

    def get_information_about_last_transfer(self):
        return self.information
