import socket
import sys
import os
import argparse
import json
import logging
import select
import time
import threading
import configparser

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMessageBox

from Project_to_OOP.common.utils import *
from Project_to_OOP.common.decorator import *
from Project_to_OOP.common.variables import *
from Project_to_OOP.descriptors import ServerPort
from Project_to_OOP.metaclass import ServerVerifier
from server.core import MessageProcessor
from Project_to_OOP.unit_tests.log_decorator import log
import log_project.config_server_log
from server.server_db import ServerDatabase
from Project_to_OOP.server.main_window import MainWindow


# Инициализация логирования сервера.
logger = logging.getLogger('server_dist')

# Флаг сигнализирует от том, что был подключён новый пользователь.
# Нужен для того, чтобы не мучать BD постоянными запросами на обновление
new_connection = False
conflag_lock = threading.Lock()


# Парсер аргументов коммандной строки.
@log
def arg_parser(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    logger.debug('Аргументы успешно загружены.')
    return listen_address, listen_port, gui_flag


# Загрузка файла конфигурации
@log
def config_load():
    """Парсер конфигурационного ini файла."""
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server_dist+++.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по
    # умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_base.db3')
        return config


@log
def main():
    '''Основная функция'''
    # Загрузка файла конфигурации сервера
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerDatabase(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Если  указан параметр без GUI то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завершаем основной цикл сервера.
                server.running = False
                server.join()
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
