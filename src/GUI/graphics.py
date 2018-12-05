# coding=utf-8
import matplotlib.patches as matches
import matplotlib.pyplot as plt

from helper.pattern.singleton import Singleton


class GraphicController(metaclass=Singleton):
    # noinspection SpellCheckingInspection
    result_graphic_type: str = "ggplot"
    from_y_limit: float = 0.000000001
    to_y_limit: float = 1.1

    def __init__(self):
        pass

    def draw_graphic(
            self,
            draw_information: list,
            coder_name: str = "",
            coder_speed: float = 1,
            start: float = 1,
            finish: int = 20
    ):
        plt.style.use(self.result_graphic_type)
        quantity_right_bits = matches.Patch(color='blue', label='Соотношение правильных символов в пакете')
        quantity_right_packages = matches.Patch(color='purple', label='Соотношение полностью правильных пакетов')
        plt.legend(handles=[quantity_right_bits, quantity_right_packages])
        plt.ylim([self.from_y_limit, self.to_y_limit])
        plt.xlim([start, finish])
        plt.semilogy(True)
        plt.ylabel("Вероятность потерь информации, P*10^-1")
        plt.xlabel("Мощность передатчика, Дб")
        step: float = (finish - start) / 20
        plt.plot([start + x * step for x in range(20)],
                 [x[5] / (x[4] + x[5]) + 0.0000001 for x in draw_information],
                 label="Кодер типа {0}\n"
                       "Скорость кодера {1}"
                 .format(coder_name, str(coder_speed)))
        plt.plot([start + x * step for x in range(20)],
                 [x[2] / (x[0] + x[1] + x[2]) + 0.0000001 for x in draw_information])
        plt.show()

    def draw_plot_pie(self, draw_information: list):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        sum_result: int = sum(draw_information)
        plt.pie(draw_information,
                labels=["Без искажений\n{0}%".format(int(draw_information[0] / sum_result * 100)),
                        "Исправленные ошибки\n{0}%".format(int(draw_information[1] / sum_result * 100)),
                        "Ошибки\n{0}%".format(int(draw_information[2] / sum_result * 100))])
        plt.title("Информация о последнем тесте")
        plt.show()
