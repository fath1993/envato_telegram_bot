"گزارش فعالیت ماهانه دوره ۱ ماهه منتهی به ۱۴۰۰/۰۱/۳۱"
import jdatetime

from custom_logs.models import custom_log

"صورت‌های مالی تلفیقی سال مالی منتهی به ۱۴۰۰/۱۲/۲۹ (حسابرسی شده)"
"اطلاعات و صورت‌های مالی میاندوره‌ای دوره ۳ ماهه منتهی به ۱۴۰۱/۰۳/۳۱ (حسابرسی نشده)"

from unidecode import unidecode
import re
import datetime
from persiantools.jdatetime import JalaliDate


def string_to_datetime(date_string):
    date_unicode = unidecode(date_string)
    # print("date_unicode: " + date_unicode)
    character_lists = remove_none_digit(date_unicode)
    digit_list = _31_to_30(character_lists)
    # print("digit_list_: " + digit_list)
    year = int(digit_list[1] + digit_list[2] + digit_list[3] + digit_list[4])
    # print("year: " + str(year))
    month = int(digit_list[5] + digit_list[6])
    # print("month: " + str(month))
    day = int(digit_list[7] + digit_list[8])
    # print("day: " + str(day))
    miladi_date = JalaliDate(year, month, day).to_gregorian()

    return datetime.date(miladi_date.year, miladi_date.month, miladi_date.day)


def string_to_date_string(date_string):
    date_unicode = unidecode(date_string)
    character_lists = remove_none_digit(date_unicode)
    digit_list = _31_to_30(character_lists)
    year = int(digit_list[1] + digit_list[2] + digit_list[3] + digit_list[4])
    month = int(digit_list[5] + digit_list[6])
    day = int(digit_list[7] + digit_list[8])

    return str(year) + "-" + str(month) + "-" + str(day)


def date_extractor(string):
    to_standard_unicode = unidecode(string)
    string_date = re.findall(r'(\d+/\d+/\d+)', to_standard_unicode)
    remove_slash = string_date[0].replace("/", " ")
    separation = remove_slash.split()
    year = separation[0]
    month = separation[1]
    day = separation[2]
    return jdatetime.date(year=int(year), month=int(month), day=int(day))


def year_extractor(string):
    to_standard_unicode = unidecode(string)
    string_date = re.findall(r'(\d+/\d+/\d+)', to_standard_unicode)
    remove_slash = string_date[0].replace("/", " ")
    separation = remove_slash.split()
    year = separation[0]
    return str(year)


def month_extractor(string):
    to_standard_unicode = unidecode(string)
    string_date = re.findall(r'(\d+/\d+/\d+)', to_standard_unicode)
    remove_slash = string_date[0].replace("/", " ")
    separation = remove_slash.split()
    month = separation[1]
    return str(month)


def day_extractor(string):
    to_standard_unicode = unidecode(string)
    string_date = re.findall(r'(\d+/\d+/\d+)', to_standard_unicode)
    remove_slash = string_date[0].replace("/", " ")
    separation = remove_slash.split()
    day = separation[2]
    return str(day)


def string_to_date_string_year(date_string):
    character_lists = remove_none_digit(date_string)
    year = int(character_lists[1] + character_lists[2] + character_lists[3] + character_lists[4])
    return str(year)


def remove_none_digit(string):
    lists = []
    for m in string:
        if m.isdigit():
            lists.append(m)
    f = ''.join(lists)
    return f


def remove_space_slash(string):
    string = string.replace("/", "")
    string = string.replace(" ", "")
    string = string.replace(":", "")
    return string


def _31_to_30(string):
    string = string.replace("31", "30")
    return string


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


def codal_title_cleanup(word_str: str):
    print(word_str)
    status_dict = {}
    word_str = word_str.replace('ي', 'ی')
    word_str = word_str.replace('آ', 'ا')
    if word_str.find('حسابرسی شده') != -1:
        status_dict['حسابرسی شده'] = True
        word_str = word_str.replace('حسابرسی شده', '')
    else:
        status_dict['حسابرسی شده'] = False

    if word_str.find('حسابرسی نشده') != -1:
        status_dict['حسابرسی نشده'] = True
        word_str = word_str.replace('حسابرسی نشده', '')
    else:
        status_dict['حسابرسی نشده'] = False

    if word_str.find('اصلاحیه') != -1:
        status_dict['اصلاحیه'] = True
        word_str = word_str.replace('اصلاحیه', '')
    else:
        status_dict['اصلاحیه'] = False
    return word_str, status_dict


def date_range_generator(year: int, month: int):
    if month == 1:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=31)]
    elif month == 2:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=31)]
    elif month == 3:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=31)]
    elif month == 4:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=31)]
    elif month == 5:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=31)]
    elif month == 6:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=31)]
    elif month == 7:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=30)]
    elif month == 8:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=30)]
    elif month == 9:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=30)]
    elif month == 10:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=30)]
    elif month == 11:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=30)]
    else:
        return [jdatetime.datetime(year=year, month=month, day=1), jdatetime.datetime(year=year, month=month, day=30)]