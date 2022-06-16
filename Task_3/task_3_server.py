import sys
import json
import argparse
import logging
import log_project.config_server_log

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from errors import IncorrectDataReceivedError

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message

SERVER_LOGGER = logging.getLogger('server')


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'LoggedUser':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv_sock.bind((listen_address, listen_port))
    serv_sock.listen(MAX_CONNECTIONS)

    while True:
        client_sock, client_address = serv_sock.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_message(client_sock)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_message(client_sock, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client_sock.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client_sock.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client_sock.close()

if __name__ == '__main__':
    main()
