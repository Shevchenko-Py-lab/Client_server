# Написать скрипт, осуществляющий выборку определенных данных из файлов
# info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.
import csv
import re
import chardet


def get_data():

    main_data = []
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for i in range(1, 4):
        with open(f'info_{i}.txt', 'rb') as f_n:
            content = f_n.read()
            result = chardet.detect(content)
            data = content.decode(result['encoding'])

        os_prod_mask = re.compile(r'Изготовитель системы:\s*\S*')
        os_name_mask = re.compile(r'Windows\s\S*')
        os_code_mask = re.compile(r'Код продукта:\s*\S*')
        os_type_mask = re.compile(r'Тип системы:\s*\S*')

        os_prod_list.append(os_prod_mask.findall(data)[0].split()[2])
        os_name_list.append(os_name_mask.findall(data)[0])
        os_code_list.append(os_code_mask.findall(data)[0].split()[2])
        os_type_list.append(os_type_mask.findall(data)[0].split()[2])

    rows = [os_prod_list, os_name_list, os_code_list, os_type_list]

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    lines = [list(i) for i in zip(*rows)]

    main_data.extend(lines)

    return main_data


def write_to_csv(out_file):

    main_data = get_data()
    with open(out_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in main_data:
            writer.writerow(row)


write_to_csv('data_report.csv')
