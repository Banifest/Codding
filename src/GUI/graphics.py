# coding=utf-8
import matplotlib.patches as matches
import matplotlib.pyplot as plt

from src.channel.enum_noise_mode import EnumNoiseMode
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
    __Y_LABEL: str = "Chance of last _information, P*10^-1"
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
        if static_collector.testResult[0].noise_type == EnumNoiseMode.SINGLE \
                or static_collector.testResult[0].noise_type == EnumNoiseMode.MIX:
            plt.xlim([static_collector.beginNoise, static_collector.endNoise])
        else:
            package_noise = abs(1 / static_collector.noiseLength * static_collector.noisePeriod) - 1
            plt.xlim(package_noise - 0.1, package_noise + 0.1)

        plt.semilogy(True)

        plt.ylabel(self.__Y_LABEL)
        plt.xlabel(self.__X_LABEL)

        noise_step_different: float = SimpleCalculationForTransferProcess.calc_noise_of_steps_different(
            start=static_collector.beginNoise,
            finish=static_collector.endNoise,
            quantity_steps=static_collector.quantityStepsInCycle
        )

        test_noise_sequence: list = []
        # Axis X - noise
        if static_collector.testResult[0].noise_type == EnumNoiseMode.SINGLE \
                or static_collector.testResult[0].noise_type == EnumNoiseMode.MIX:
            test_noise_sequence: list = [
                static_collector.beginNoise + number_of_step * noise_step_different
                for number_of_step in range(static_collector.quantityStepsInCycle)
            ]
        else:
            test_noise_sequence: list = [
                package_noise + number_of_step * 0.01 - 0.1
                for number_of_step in range(static_collector.quantityStepsInCycle)
            ]
        # Plot _information about transfer packages
        plt.plot(
            test_noise_sequence,
            # Axis Y - result of test (Package)
            [test_result.error_packages
             / (test_result.error_packages + test_result.repair_packages + test_result.successful_packages)
             + (self.__FROM_Y_LIMIT * 1.1) for test_result in static_collector.testResult],
            color='blue',
        )

        # # Plot _information about transfer bits
        # plt.plot(
        #     test_noise_sequence,
        #     # Axis Y - result of test (Bits)
        #     [x.quantity_error_bits / x.quantity_correct_bits + self.__FROM_Y_LIMIT for x in
        #      static_collector.testResult],
        # )

        # Plot _information about transfer based bits
        plt.plot(
            test_noise_sequence,
            # Axis Y - result of test (Bits)
            [x.based_error_bits / (x.based_error_bits + x.based_correct_bits) + (self.__FROM_Y_LIMIT * 1.1) for x in
             static_collector.testResult],
            color='red',
        )
        plt.show()
