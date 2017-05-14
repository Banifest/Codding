from src.GUI.windows.MainWindow import InitMainWindow
from src.logger import log



if __name__ == '__main__':
    try:
        log.info("Начало работы программы")
        InitMainWindow()
        log.info("Конец работы программы")
    except:
        log.critical("Необрабатываемое исключение")
        pass
else:
    raise Exception()
