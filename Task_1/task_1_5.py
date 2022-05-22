# Написать код, который выполняет пинг веб - ресурсов yandex.ru, youtube.com и преобразовывает результат
# из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.

import subprocess
import platform
from chardet import detect

OS_check = '-n' if platform.system().lower() == 'windows' else '-c'

first_url = 'yandex.ru'
second_url = 'youtube.com'

url_list = [first_url, second_url]

for ping_url in url_list:
    args = ['ping', OS_check, '4', ping_url]
    ping_process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for response in ping_process.stdout:
        output = detect(response)
        print(output)
        response = response.decode(output['encoding']).encode('utf-8')
        print(response.decode('utf-8'))
