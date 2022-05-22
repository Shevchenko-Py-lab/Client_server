# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

def encoding(list_of_words):
    new_list_of_words = []
    for word in list_of_words:
        word_to_bytes = word.encode('utf-8')
        print(word_to_bytes)
        bytes_back_to_word = bytes.decode(word_to_bytes, encoding='utf-8')
        new_list_of_words.append(new_list_of_words)
    print('{:*^30}'.format('End of list'))
    return new_list_of_words


first_word = 'разработка'
second_word = 'администрирование'
third_word = 'protocol'
fourth_word = 'standard'

word_list = [first_word, second_word, third_word, fourth_word]

encoding(word_list)
