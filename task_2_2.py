# Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными.


import json
from pprint import pprint


def write_order_to_json(item: str, quantity: str, price: str, buyer: str, date: str):

    with open('orders.json', 'r', encoding='utf-8') as f_output:
        data = json.load(f_output)

    with open('orders.json', 'w', encoding='utf-8') as f_input:
        orders_list = data['orders']
        order = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        }
        orders_list.append(order)
        json.dump(data, f_input, indent=4, ensure_ascii=False)

    return


write_order_to_json('стул', '12', '100', 'Воробьянинов', '24.10.1930')

with open('orders.json', encoding='utf-8') as f_n:
    OBJ = json.load(f_n)
    pprint(OBJ)
