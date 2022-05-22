# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной
# кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.

from chardet import detect

word_list = ['сетевое программирование', 'сокет', 'декоратор']
with open('word_lst.txt', 'w', encoding='utf-8') as file:
    for word in word_list:
        file.write(f'{word}\n')
file.close()


with open('word_lst.txt', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']
print('encoding: ', encoding)

with open('word_lst.txt', 'r', encoding=encoding) as file:
    content = file.read()
print(content)
