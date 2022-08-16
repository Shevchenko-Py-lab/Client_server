import logging

from Project_to_OOP.common.variables import DEFAULT_PORT

logger = logging.getLogger('server_desc')


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
