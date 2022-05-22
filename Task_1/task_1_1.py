# Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и
# содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые
# представление в формат Unicode и также проверить тип и содержимое переменных.

def str_view_type_check(list_of_words):
    for word in list_of_words:
        print(word, type(word))
    print('{:*^30}'.format('End of list'))
    return


first_word = 'разработка'
second_word = 'сокет'
third_word = 'декоратор'
word_list = [first_word, second_word, third_word]

str_view_type_check(word_list)

first_word = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
second_word = '\u0441\u043e\u043a\u0435\u0442'
third_word = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

word_list = [first_word, second_word, third_word]

str_view_type_check(word_list)
