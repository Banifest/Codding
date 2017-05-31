from brewer2mpl import brewer2mpl
from matplotlib import rcParams
from pandas import DataFrame


def InitGraphics():
    # colorbrewer2 Dark2 qualitative color table
    dark2_colors = brewer2mpl.get_map('Dark2', 'Qualitative', 7).mpl_colors

    rcParams['figure.figsize'] = (10, 6)
    rcParams['figure.dpi'] = 150
    rcParams['axes.color_cycle'] = dark2_colors
    rcParams['lines.linewidth'] = 2
    rcParams['axes.facecolor'] = 'white'
    rcParams['font.size'] = 14
    rcParams['patch.edgecolor'] = 'white'
    rcParams['patch.facecolor'] = dark2_colors[0]
    rcParams['font.family'] = 'StixGeneral'

def DrawGraphic(drawInformation: list):
    import matplotlib.pyplot as plt
    InitGraphics()


    def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
        ax = axes or plt.gca()
        ax.spines['top'].set_visible(top)
        ax.spines['right'].set_visible(right)
        ax.spines['left'].set_visible(left)
        ax.spines['bottom'].set_visible(bottom)

        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticks_position('none')

        if top:
            ax.xaxis.tick_top()
        if bottom:
            ax.xaxis.tick_bottom()
        if left:
            ax.yaxis.tick_left()
        if right:
            ax.yaxis.tick_right()

    df2 = DataFrame(drawInformation,
                    columns=["Без искажений", "Исправленные ошибки", "Обнаруженные ошибки", "Необнаруженные ошибки"])
    df2.plot(kind='bar', stacked=True)
    plt.xlabel("Шанс на искажение бита информации, %")
    plt.ylabel("Количество тестов")
    plt.show()


def DrawPlotPie(drawInformation: list):
    import matplotlib.pyplot as plt

    InitGraphics()

    fig = plt.figure()
    sumResult: int = sum(drawInformation)
    plt.pie(drawInformation, labels=[
        "Без искажений\n{0}".format(drawInformation[0] / sumResult * 100),
        "Исправленные ошибки\n{0}".format(drawInformation[1] / sumResult * 100),
        "Ошибки\n{0}".format(drawInformation[2] / sumResult * 100)])
    plt.title("Информация о последнем тесте")
    plt.show()
