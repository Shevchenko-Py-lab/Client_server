# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
# Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.

def bytes_view_type_check(list_of_words):
    for word in list_of_words:
        try:
            word_bytes_type = eval(f"b'{word}'")
            print(word_bytes_type, type(word_bytes_type))

        except SyntaxError:
            print(f'word "{word}" is not possible to write in bytes, '
                  f'as bytes can only contain ASCII literal characters')
        finally:
            print('next word:')

    print('{:*^30}'.format('End of list'))
    return


first_word = 'attribute'
second_word = 'класс'
third_word = 'функция'
fourth_word = 'type'

word_list = [first_word, second_word, third_word, fourth_word]

bytes_view_type_check(word_list)
