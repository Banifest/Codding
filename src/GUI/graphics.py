# coding=utf-8
import matplotlib.patches as matches
import matplotlib.pyplot as plt

from src.helper.calc.simple_calculation_for_transfer_process import SimpleCalculationForTransferProcess
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
        noise_step_different: float = SimpleCalculationForTransferProcess.calc_noise_of_steps_different(
            start=static_collector.beginNoise,
            finish=static_collector.endNoise,
            quantity_steps=static_collector.quantity_of_steps_in_cycle
        )

        # Plot information about transfer packages
        plt.plot([static_collector.beginNoise + number_of_step * noise_step_different for number_of_step in
                  range(static_collector.quantity_of_steps_in_cycle)],
                 [test_result.error_packages
                  / (test_result.error_packages + test_result.repair_packages + test_result.successful_packages)
                  + 10 ** (-10) for test_result in
                  static_collector.testResult],
                 label="Кодер типа {0}\n"
                       "Скорость кодера {1}"
                 .format("Test", "Test"))

        # Plot information about transfer bits
        plt.plot([static_collector.beginNoise + number_of_step * noise_step_different for number_of_step in
                  range(static_collector.quantity_of_steps_in_cycle)],
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
