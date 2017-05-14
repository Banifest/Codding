from src.GUI.windows.MainWindow import InitMainWindow
from src.logger import log



if __name__ == '__main__':
    try:
        # a = hemming.Coder.Coder(10)
        # print(a.Decoding([0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1]))
        log.info("Начало работы программы")
        InitMainWindow()
        log.info("Конец работы программы")
    except Exception as e:
        print(e)
        log.critical("Необрабатываемое исключение")
        pass
else:
    raise Exception()
