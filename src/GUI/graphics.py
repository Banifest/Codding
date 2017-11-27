import matplotlib.pyplot as plt


# noinspection SpellCheckingInspection
# def init_graphics():
#     dark2_colors = brewer2mpl.get_map('Dark2', 'Qualitative', 7).mpl_colors
#
#     rcParams['figure.figsize'] = (10, 6)
#     rcParams['figure.dpi'] = 150
#     rcParams['axes.color_cycle'] = dark2_colors
#     rcParams['lines.linewidth'] = 2
#     rcParams["axes.facecolor"] = 'white'
#     rcParams['font.size'] = 14
#     rcParams['patch.edgecolor'] = 'white'
#     rcParams['patch.facecolor'] = dark2_colors[0]
#     rcParams['font.family'] = 'StixGeneral'


def draw_graphic(draw_information: list, coder_name: str = "", coder_speed=1):
    plt.style.use('ggplot')
    plt.legend()
    plt.ylim([0.0000001, 1])
    plt.xlim([0, 20])
    plt.semilogy(True)
    plt.ylabel("Шанс на искажение бита информации, P*10^-1")
    plt.xlabel("Мошность передатчика в Дб")

    print([x[5] / (x[4] + x[5]) + 0.00001 for x in draw_information])
    plt.plot(range(20)[::-1],
             [x[5] / (x[4] + x[5]) + 0.0000001 for x in draw_information],
             label="Кодер типа {0}\n"
                   "Скорость кодера {1}"
             .format(coder_name, str(coder_speed)))
    #    plt.plot([x[0] + x[1] for x in draw_information])
    plt.show()


def draw_plot_pie(draw_information: list):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    sumResult: int = sum(draw_information)
    plt.pie(draw_information,
            labels=["Без искажений\n{0}%".format(int(draw_information[0] / sumResult * 100)),
                    "Исправленные ошибки\n{0}%".format(int(draw_information[1] / sumResult * 100)),
                    "Ошибки\n{0}%".format(int(draw_information[2] / sumResult * 100))])
    plt.title("Информация о последнем тесте")
    plt.show()
