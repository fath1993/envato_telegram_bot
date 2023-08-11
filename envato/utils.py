import re

import requests

from custom_logs.models import custom_log
from envato.models import get_envato_telegram_bot_config_settings


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



def telegram_http_send_message(user_id, message):
    try:
        req = requests.get(url='https://api.telegram.org/bot' + get_envato_telegram_bot_config_settings().bot_token + '/sendMessage?chat_id=' + str(user_id) + '&text=' + str(message))
        custom_log('telegram_http_send_message-> message: ' + str(req.content))
    except Exception as e:
        custom_log('telegram_http_send_message->try/except. err: ' + str(e))
