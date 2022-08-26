"""Программа-лаунчер"""

import subprocess

process = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        # Запускаем сервер!
        process.append(subprocess.Popen('python task_3_server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        # Запускаем клиентов:
        for i in range(clients_count):
            process.append(
                subprocess.Popen(f'python task_3_client.py -n test{i + 1}', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while process:
            process.pop().kill()
