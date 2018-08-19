# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_graphic(draw_information: list, coder_name: str = "", coder_speed=1, start: float = 1, finish: int = 20):
    plt.style.use('ggplot')
    quantity_right_bits = mpatches.Patch(color='blue', label='Соотношение правильных символов в пакете')
    quantity_right_packages = mpatches.Patch(color='purple', label='Соотношение полностью правильных пакетов')
    plt.legend(handles=[quantity_right_bits, quantity_right_packages])
    plt.ylim([0.0000001, 1.1])
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


def draw_plot_pie(draw_information: list):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    sum_result: int = sum(draw_information)
    plt.pie(draw_information,
            labels=["Без искажений\n{0}%".format(int(draw_information[0] / sum_result * 100)),
                    "Исправленные ошибки\n{0}%".format(int(draw_information[1] / sum_result * 100)),
                    "Ошибки\n{0}%".format(int(draw_information[2] / sum_result * 100))])
    plt.title("Информация о последнем тесте")
    plt.show()
