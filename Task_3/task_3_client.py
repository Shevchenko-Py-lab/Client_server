import sys
import json
import time
import argparse
import logging
import log_project.config_client_log
from errors import ReqFieldMissingError

from common.utils import get_message, send_message

from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS,\
    DEFAULT_PORT
from log_decorator import log

LOGGER = logging.getLogger('client')


@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.localtime(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


@log
def process_ans(message):
    LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


@log
def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    if not 1023 < server_port < 65536:
        LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address} , порт: {server_port}')

    try:
        client_sock = socket(AF_INET, SOCK_STREAM)
        client_sock.connect((server_address, server_port))
        message_to_server = create_presence('LoggedUser')
        send_message(client_sock, message_to_server)
        answer = process_ans(get_message(client_sock))
        LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ConnectionRefusedError:
        LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
    except ReqFieldMissingError as missing_error:
        LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')


if __name__ == '__main__':
    main()
