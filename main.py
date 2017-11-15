from GUI.controller.MainController import MainController

# from src.logger import log

if __name__ == '__main__':
    try:
        #        log.info("Начало работы программы")
        controller = MainController()
    #        log.info("Конец работы программы")
    except Exception as e:
        print(e)
#        log.critical("Необработанное исключение")
else:
    raise Exception("Невозможен import данного файла:(")
