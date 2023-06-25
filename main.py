import re
from pprint import pprint
import csv

with open("phonebook_raw.csv",  encoding='utf-8') as f:
    rows = csv.reader(f)
    contacts_list = list(rows)

headers = contacts_list.pop(0)
new_list = []
for row in contacts_list:
    for item in row:
        if item not in new_list:
            new_list.append(item)

new_list.remove("")
pprint(new_list)


new_str = ",".join(new_list)
# print(new_str)
# приведение телефонов к общему виду
pattern_phones_with_add = r"(\+7|8)?\s?(\(?[4-9]{1}[4-9]{1}[4-9]{1}[\)]?)[\s-]?(\d+)[\s-]?(\d+)[\s-]?(\d+)[\s]*[\(]?([б-о]+[\.]+)[\s*\d+\)+](\d+)[\)]?"
pattern_simple_phone = r"(\+7|8)?\s?(\(?([4-9]{1}[4-9]{1}[4-9]{1})[\)-]?)[\s-]?(\d{3})[\s-]?(\d{2})[-]?(\d+)"
subst_replacement_with_add = r"+7\2\3-\4-\5 \6\7"
subst_for_simple = r"+7(\3)\4-\5-\6"

result = re.sub(pattern_phones_with_add, subst_replacement_with_add, new_str)
result2 = re.sub(pattern_simple_phone, subst_for_simple, result)

# приведение ФИО к общему виду через запятую
pattern_names = r"([А-ЯЁ][а-яё]+\s)([А-ЯЁ][а-яё]+\s*)([А-ЯЁ][а-яё]+)"
subst_for_names = r"\1,\2,\3"

result4 = re.sub(pattern_names, subst_for_names, result2)
while " ," in result4:
    result4 = result4.replace(" ,", ",")  # для удаления лишних пробелов перед запятой
# pprint(result4)

# паттерн для приведение к общему виду Ивана Лагунцова, поскольку он не вписывался в предыдущие паттерны
pattern_names_Ivan = r"([А-ЯЁ][а-яё]+\s)([А-ЯЁ][а-яё]+)"
subst_for_Ivan = r"\1,\2"
result5 = re.sub(pattern_names_Ivan, subst_for_Ivan, result4)
while " ," in result5:
    result5 = result5.replace(" ,", ",")

# окончательный вариант списка
result_finish = []
result_list = result5.split(',')
for item in result_list:
    if item not in result_finish:
        result_finish.append(item)
    else:
        continue
pprint(result_finish)

# попытка привести к более читаемому виду, но неудачная
# pattern_finish = r"([\s?*'][А-ЯЁ][а-яё]+['$]{1})"
# subst_finish = r"\n\1"
# result_finish =re.sub(pattern_finish, subst_finish, str(result_finish))
# result_finish = result_finish.split(',')
# # pprint(result_finish)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(headers)
    datawriter.writerow([result_finish])
