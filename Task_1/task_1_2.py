# Каждое из слов «class », «function», «method» записать в байтовом типе.Сделать это необходимо в автоматическом,
# а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е.ни в коем случае не используя методы
# encode, decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.

def bytes_view_type_check(list_of_words):
    for word in list_of_words:
        word_bytes_type = eval(f"b'{word}'")
        print(f'слово {word}', f', байт = {len(word_bytes_type)}', type(word_bytes_type))
    print('{:*^30}'.format('End of list'))
    return


first_word = 'class'
second_word = 'function'
third_word = 'method'
word_list = [first_word, second_word, third_word]

bytes_view_type_check(word_list)
