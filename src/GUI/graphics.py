# coding=utf-8
import matplotlib.patches as matches
import matplotlib.pyplot as plt

from src.helper.calc.simple_calculation_for_transfer_process import SimpleCalculationForTransferProcess
from src.helper.pattern.singleton import Singleton
from src.statistics.object.statistic_collector import StatisticCollector


class GraphicController(metaclass=Singleton):
    # noinspection SpellCheckingInspection
    __RESULT_GRAPHIC_TYPE: str = "ggplot"
    __CORRECT_PACKAGE: str = "Quantity of incorrect packages"
    __CORRECT_BITS: str = "Quantity of incorrect bits"
    __SOURCE_CORRECT_BITS: str = "Quantity of source incorrect bits"
    __FROM_Y_LIMIT: float = 10 ** (-10)
    __TO_Y_LIMIT: float = 1.1
    __Y_LABEL: str = "Chance of last information, P*10^-1"
    __X_LABEL: str = "Power of signal, Db"

    def draw_graphic(
            self,
            static_collector: StatisticCollector
    ):
        """
        :param static_collector: StatisticCollector
        """
        plt.style.use(self.__RESULT_GRAPHIC_TYPE)
        plt.legend(handles=[
            matches.Patch(color='blue', label=GraphicController.__CORRECT_PACKAGE),
            # matches.Patch(color='purple', label=GraphicController.__CORRECT_BITS),
            matches.Patch(color='red', label=GraphicController.__SOURCE_CORRECT_BITS),
        ])
        plt.ylim([self.__TO_Y_LIMIT, self.__FROM_Y_LIMIT])
        plt.xlim([static_collector.beginNoise, static_collector.endNoise])
        plt.semilogy(True)

        plt.ylabel(self.__Y_LABEL)
        plt.xlabel(self.__X_LABEL)

        noise_step_different: float = SimpleCalculationForTransferProcess.calc_noise_of_steps_different(
            start=static_collector.beginNoise,
            finish=static_collector.endNoise,
            quantity_steps=static_collector.quantity_of_steps_in_cycle
        )

        # Axis X - noise
        test_noise_sequence: list = [
            static_collector.beginNoise + number_of_step * noise_step_different
            for number_of_step in range(static_collector.quantity_of_steps_in_cycle)
        ]
        # Plot information about transfer packages
        plt.plot(
            test_noise_sequence,
            # Axis Y - result of test (Package)
            [test_result.error_packages
             / (test_result.error_packages + test_result.repair_packages + test_result.successful_packages)
             + self.__FROM_Y_LIMIT for test_result in static_collector.testResult],
            color='blue',
        )

        # # Plot information about transfer bits
        # plt.plot(
        #     test_noise_sequence,
        #     # Axis Y - result of test (Bits)
        #     [x.quantity_error_bits / x.quantity_correct_bits + self.__FROM_Y_LIMIT for x in
        #      static_collector.testResult],
        # )

        # Plot information about transfer based bits
        plt.plot(
            test_noise_sequence,
            # Axis Y - result of test (Bits)
            [x.based_error_bits / (x.based_error_bits + x.based_correct_bits) + self.__FROM_Y_LIMIT for x in
             static_collector.testResult],
            color='red',
        )
        plt.show()
