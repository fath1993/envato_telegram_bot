import re


def word_simplifier(word_str, space_status=None):
    regex_word_str = re.sub(r"\d{4}/\d{2}/\d{2}", "", word_str)
    word_str = str(regex_word_str)

    word_str = word_str.replace('ي', 'ی')
    word_str = word_str.replace('آ', 'ا')
    word_str = word_str.replace('(', '')
    word_str = word_str.replace(')', '')
    word_str = word_str.replace('.', '')
    word_str = word_str.replace('..', '')
    word_str = word_str.replace(',', '')
    word_str = word_str.replace(',,', '')
    word_str = word_str.replace('|', '')
    word_str = word_str.replace('||', '')
    word_str = word_str.replace('?', '')
    word_str = word_str.replace('??', '')
    word_str = word_str.replace('!', '')
    word_str = word_str.replace('!!', '')
    word_str = word_str.replace('/', '')
    word_str = word_str.replace('//', '')
    word_str = word_str.replace('\\', '')
    word_str = word_str.replace('    ', '')
    word_str = word_str.replace('   ', '')
    word_str = word_str.replace('  ', '')
    if space_status == 'without_space':
        word_str = word_str.replace(' ', '')
    return word_str

