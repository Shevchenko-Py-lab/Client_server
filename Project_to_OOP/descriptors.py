import logging
import sys

from Project_to_OOP.common.variables import DEFAULT_PORT

# Инициализиция логера
# метод определения модуля, источника запуска.
if sys.argv[0].find('client_dist') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server_dist')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client_dist')


class ServerPort:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Порта {value} недопустим. Допустимые адреса портов 1024 - 65535. Порт по умолчанию {DEFAULT_PORT}'
            )

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name
