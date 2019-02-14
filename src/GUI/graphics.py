# coding=utf-8
import matplotlib.patches as matches
import matplotlib.pyplot as plt

from src.helper.pattern.singleton import Singleton
from src.statistics.object.statistic_collector import StatisticCollector


class GraphicController(metaclass=Singleton):
    # noinspection SpellCheckingInspection
    RESULT_GRAPHIC_TYPE: str = "ggplot"
    _from_y_limit: float = 10 ** (-10)
    _to_y_limit: float = 1.1

    def __init__(self):
        pass

    def draw_graphic(
            self,
            static_collector: StatisticCollector
    ):
        """
        :param static_collector: StatisticCollector
        """
        plt.style.use(self.RESULT_GRAPHIC_TYPE)
        plt.legend(handles=[
            matches.Patch(color='blue', label='Соотношение правильных символов в пакете'),
            matches.Patch(color='purple', label='Соотношение полностью правильных пакетов')
        ])
        plt.ylim([self._to_y_limit, self._from_y_limit])
        plt.xlim([static_collector.beginNoise, static_collector.endNoise])
        plt.semilogy(True)
        plt.ylabel("Вероятность потерь информации, P*10^-1")
        plt.xlabel("Мощность передатчика, Дб")
        step: float = (static_collector.endNoise - static_collector.beginNoise) / 20

        #

        plt.plot([static_collector.beginNoise + x * step for x in range(20)],
                 [x.error_packages / (x.error_packages + x.repair_packages + x.successful_packages)
                  + 10 ** (-20) for x in
                  static_collector.testResult],
                 label="Кодер типа {0}\n"
                       "Скорость кодера {1}"
                 .format("Test", "Test"))
        plt.plot([static_collector.beginNoise + x * step for x in range(20)],
                 [x.quantity_error_bits / x.quantity_correct_bits + self._from_y_limit for x in
                  static_collector.testResult])
        plt.show()

    def draw_plot_pie(self, draw_information: list):
        """
        TODO
        :param draw_information:
        """
        plt.figure()
        sum_result: int = sum(draw_information)
        plt.pie(draw_information,
                labels=["Без искажений\n{0}%".format(int(draw_information[0] / sum_result * 100)),
                        "Исправленные ошибки\n{0}%".format(int(draw_information[1] / sum_result * 100)),
                        "Ошибки\n{0}%".format(int(draw_information[2] / sum_result * 100))])
        plt.title("Информация о последнем тесте")
        plt.show()
