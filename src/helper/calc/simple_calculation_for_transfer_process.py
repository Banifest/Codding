# coding=utf-8


class SimpleCalculationForTransferProcess:

    @staticmethod
    def calc_noise_of_steps_different(start: float, finish: float, quantity_steps: int) -> float:
        """
        Method provide functionality for determination step of noise for cycle package transfer test
        :param start: int
        :param finish: int
        :param quantity_steps: int
        :return: float
        """
        return (finish - start) / (quantity_steps - 1)
