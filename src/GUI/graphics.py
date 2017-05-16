from brewer2mpl import brewer2mpl
from matplotlib import rcParams
from pandas import DataFrame



def DrawGraphic(drawInformation: list):
    import matplotlib.pyplot as plt


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


    def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
        """
        Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks

        The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
        """
        ax = axes or plt.gca()
        ax.spines['top'].set_visible(top)
        ax.spines['right'].set_visible(right)
        ax.spines['left'].set_visible(left)
        ax.spines['bottom'].set_visible(bottom)

        # turn off all ticks
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticks_position('none')

        # now re-enable visibles
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
    plt.show()
