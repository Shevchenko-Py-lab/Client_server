import sys
import logging
import Project_to_OOP.log_project.config_server_log
import Project_to_OOP.log_project.config_client_log
import traceback
import inspect

# метод определения модуля, источника запуска.
if sys.argv[0].find('client_dist') == -1:
    LOGGER = logging.getLogger('server_dist')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client_dist')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret
    return log_saver
