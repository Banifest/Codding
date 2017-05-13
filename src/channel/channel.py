import random
from typing import Optional

from src.coders import abstractCoder
from src.coders.exeption import DecodingException
from src.coders.interleaver import Interleaver


class Channel:
    noiseProbability: int = 0  # вероятность ошибки
    countCyclical: int = 1
    duplex: bool = False
    information: str = ""
    coder: abstractCoder.Coder
    interleaver: Interleaver.Interleaver = False

    countSuccessfullyMessage: int

    # LDPC

    def __init__(self, coder: abstractCoder.Coder, noiseProbability: Optional[int], countCyclical: Optional[int],
                 duplex: Optional[bool], interleaver: Optional[Interleaver.Interleaver]):
        self.coder = coder
        if noiseProbability is not None: self.noiseProbability = int(noiseProbability * 100)
        if countCyclical is not None: self.countCyclical = countCyclical
        if duplex is not None: self.duplex = duplex
        if duplex is not None: self.interleaver = interleaver

    def __str__(self) -> str:
        return "Вероятность ошибки в канале - {0}.\n"\
               "Является ли канал двухстаронним - {1}.\n"\
               "Используеммый кодер:\n {2}."\
               "Используется ли перемежитель на данном канале связи - {3}.\n"\
               "Количество циклов передачи пакета - {4}\n"\
               "Информация о последней передаче:\n{5}".format(
                self.noiseProbability,
                "Да" if self.duplex else "Нет",
                str(self.coder),
                "Нет" if not self.interleaver else "Да",
                self.countCyclical,
                self.information
                )

    def Transfer(self, information: list) -> str:
        countSuccessfully: int = 0
        self.information += "Начата циклическая передача пакета ({0}).\n Количество передач {1}.\n".\
            format(information, self.countCyclical)

        for x in range(self.countCyclical):
            try:
                nowInformation: list = information
                nowInformation = self.coder.Encoding(nowInformation)
                if self.interleaver: nowInformation = self.interleaver.Shuffle(nowInformation)
                nowInformation = self.GenInterference(nowInformation)
                if self.interleaver: nowInformation = self.interleaver.Reestablish(nowInformation)
                nowInformation = self.coder.Decoding(nowInformation)
            except DecodingException:
                self.information += "Пакет при передаче попыткой под номером {0} был повреждён и не подлежит "\
                                    "востановлению\n".format(x)
            else:
                if nowInformation == information:
                    countSuccessfully += 1
                    self.information += "Пакет при передаче попыткой под номером {0} был успешно передан\n".format(x)
                else:
                    self.information += "Пакет при передаче попыткой под номером {0} был повреждён и не подлежит "\
                                        "востановлению\n".format(x)

        self.information += "Циклическая передача пакета ({0}) завершена.\n"\
                            "Всего попыток передать пакет {1}.\n"\
                            "Количство успешно переданных пакетов {2}.\n"\
                            "Количество неудачно переданных пакетов {3}.\n".\
            format(information, self.countCyclical, countSuccessfully, self.countCyclical - countSuccessfully)

        return self.information


    def TransferOneStep(self, information: list) -> str:
        try:
            nowInformation: list = information
            nowInformation = self.coder.Encoding(nowInformation)
            if self.interleaver: nowInformation = self.interleaver.Shuffle(nowInformation)
            nowInformation = self.GenInterference(nowInformation, self.noiseProbability)
            if self.interleaver: nowInformation = self.interleaver.Reestablish(nowInformation)
            nowInformation = self.coder.Decoding(nowInformation)
        except DecodingException:
            self.information = "Пакет при передаче был повреждён и не подлежит "\
                               "востановлению\n"
        else:
            if nowInformation == information:
                self.information = "Пакет при передаче был успешно передан\n"
            else:
                self.information = "Пакет при передаче был повреждён и не подлежит "\
                                   "востановлению\n"

        return self.information


    def GetInformationAboutLastTransfer(self):
        return self.information

    def GenInterference(self, information: list, straight: Optional[float]) -> list:
        """
        Генерация помех с задданной вероятностью
        :param information: list Информация, представленная в виде массива битов
        :param straight: Optional[float] Вероятность помех принимает значения от 0.00 до 100.00, может быть опушенна, 
        в таком случае будет использоваться значение шума заданное в канале  
        :return: Искажённую информацию, представленную в виде массива битов
        """
        randomGenerator: random.Random = random.Random(random.random() * 50)  # генератор случайных чисел
        if straight is None: straight = self.noiseProbability
        answer: list = []
        straight = int(straight * 100)
        for x in information:
            if randomGenerator.randint(0, 10000) < straight:
                answer.append(x * randomGenerator.getrandbits(1))
            else:
                answer.append(x)
        return answer
