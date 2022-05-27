# Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле

import yaml

input_dict = {'list': ['first', 'second', 'third'],
              'integer': 5,
              'dict_in_dict': {'first': '1$',
                               'second': '2€'}
              }

with open('data.yaml', 'w', encoding='utf-8') as f_in:
    yaml.dump(input_dict, f_in, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open("data.yaml", 'r', encoding='utf-8') as f_out:
    output = yaml.load(f_out, Loader=yaml.SafeLoader)

print(input_dict == output)
