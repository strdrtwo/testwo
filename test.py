import os
import shutil
import time
import logging


firstdir = input('Введите путь к каталогу источнику: ')
seconddir = input('Введите путь к каталогу реплике: ')
logfile = input('Введите путь к файлу логгирования: ')
delay = int(input('Введите интервал синхронизации в секундах: '))

namefile = set()  # Перечень файлов записанных в каталог-реплику
namedir = set()  # Перечень каталогов записанных в каталог-реплику


'''Создание логгера'''
logger = logging.getLogger('mylog')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(logfile + '.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


logger.info("Program started")

'''Создание файлов и папок'''
def f1(directory, dirtwo):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            file = os.path.join(dirtwo, os.path.relpath(path, firstdir))
            '''Проверка на наличие файла в каталоге'''
            if os.path.exists(file) is True:
                pass
            else:
                namefile.add(path)
                logger.info('file created {} '.format(path))
                shutil.copy(path, file)
        elif os.path.isdir(path):
            dir = os.path.join(dirtwo, os.path.relpath(path, firstdir))
            namedir.add(path)
            if os.path.exists(dir) is True:
                pass
            else:
                try:
                    logger.info('dir created {} '.format(path))
                    os.mkdir(dir)
                except FileExistsError:
                    pass
            f1(path, dirtwo)

'''Удаление файлов и папок'''
def f2(listdir, listfile):
    '''Удаление папок'''
    for path in list(listdir):
        dir = (os.path.relpath(path, firstdir))  # Удаляю корень из пути
        if os.path.exists(path) is True:  # Проверка на существование папки
            pass
        else:
            try:
                listdir.remove(path)
                logger.info('dir deleted {} '.format(path))
                shutil.rmtree(os.path.join(seconddir, dir))  # Создаю путь на папку в каталоге-реплике
            except KeyError:
                pass
            except FileNotFoundError:
                pass
            except PermissionError:
                pass
    '''Удаление файлов'''
    for path in list(listfile):
        file = (os.path.relpath(path, firstdir))  # Удаляю корень из пути
        if os.path.exists(path) is True:
            pass
        else:
            try:
                logger.info('file deleted {} '.format(path))
                listfile.remove(path)
                os.remove(os.path.join(seconddir, file))  # Создаю путь на файл в каталоге-реплике
            except KeyError:
                pass
            except FileNotFoundError:
                pass


while True:
    f1(firstdir, seconddir)
    f2(namedir, namefile)
    time.sleep(delay)
