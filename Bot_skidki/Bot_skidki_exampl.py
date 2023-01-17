"""Бот - магазин скидок.
Админ добавляет в Google Sheets магазины/сервисы со скидками и условиями.
Бот из таблицы генерирует меню с навигацией по категориям для пользователя
и выдаёт карточки со скидками.
Есть статистика общих и уникальных просмотров рубрик и магазинов/сервисов.
"""

import telebot
from telebot import types, TeleBot
import gspread

from config import TOKEN
from config import GOOGLE_JSON
from config import TABLE_URL


def strip_item(itm):
    string_item = itm.strip(' ')
    return string_item


def keys_dynamic(cat, flag):
    global len_lol
    keys_mass_dynamic = []
    markup_dynamic = types.InlineKeyboardMarkup()
    if flag == "1":
        for j in range(1, len_lol):
            if cat == strip_item(list_of_lists[j][8]):
                key_item = strip_item(list_of_lists[j][0])
                keys_mass_dynamic.append(key_item)
        keys_mass_dynamic = set(keys_mass_dynamic)
        for m in keys_mass_dynamic:
            markup_dynamic.add(types.InlineKeyboardButton(m, callback_data="2" + m))
    if flag == "2":
        markup_dynamic.add(types.InlineKeyboardButton(cat, callback_data='1' + cat))
    markup_dynamic.add(types.InlineKeyboardButton("Вернуться в меню", callback_data='3'))
    return markup_dynamic


def f_cat(c):  # Извлекаем категорию
    c = c[1:]
    return c


def f_flag(f):  # Извлекаем флаг клавиатуры
    f = f[0]
    return f


def market(marketname, id_x):   # Магазин, вывод предложений
    global len_lol
    bot.send_message(id_x, 'Чтобы успешно активировать промокод👌 \nдостаточно: перейти по ссылке или '
                           '\nскопировать значение купона с данной \nстраницы и ввести его на сайте компании☺️')
    cat = ''
    for i in range(1, len_lol):
        if marketname == strip_item(list_of_lists[i][0]):
            body_text = ''
            end_line = ''
            if list_of_lists[i][0] is not None or list_of_lists[i][0] != '':
                body_text += 'Название: ' + list_of_lists[i][0]
            if list_of_lists[i][3] is not None or list_of_lists[i][3] != '':
                body_text += '\nСкидка: ' + list_of_lists[i][3]
            if list_of_lists[i][7] is not None or list_of_lists[i][7] != '':
                body_text += '\nОписание: ' + list_of_lists[i][7]
            if list_of_lists[i][5] is not None or list_of_lists[i][5] != '':
                body_text += '\nДействует до: ' + list_of_lists[i][5]
            if list_of_lists[i][6] is not None or list_of_lists[i][6] != '':
                body_text += '\nРегион: ' + list_of_lists[i][6]
            if list_of_lists[i][4] is not None or list_of_lists[i][4] != '':
                body_text += '\nСсылка: ' + list_of_lists[i][4] + '\nПромокод ниже👇'
            cat = strip_item(list_of_lists[i][8])
            if list_of_lists[i][2] is not None or list_of_lists[i][2] != '':
                end_line += list_of_lists[i][2]
            bot.send_message(id_x, body_text)
            bot.send_message(id_x, end_line)
    stat_adding(marketname, id_x)
    return cat


def stat_adding(market, user_id):
    global stat_massive, cat_main
    r = 0
    for s in stat_massive:
        if market == stat_massive[r][0]:
            stat_massive[r][1] += [str(user_id)]
            break
        r += 1
        print('stat_massive[', r, '][0]: ', stat_massive[r][0], stat_massive[r])
        print('stat_massive: ', stat_massive)


def stat_cat_add(category, user_id):
    global stat_cat
    m = 0
    for h in stat_cat:
        if category == stat_cat[m][0]:
            stat_cat[m][1] += [str(user_id)]
            break
        m += 1


def stat_cat_print():
    global stat_cat
    text = ''
    str1 = 'Название категории: '
    str2 = 'Количество кликов: '
    str3 = 'Количество уникальных пользователей: '
    z = 0
    for name in stat_cat:
        if len(stat_cat[z][1]) > 0:
            text += str1 + stat_cat[z][0] + '\n'
            text += str2 + str(len(stat_cat[z][1])) + '\n'
            text += str3 + str(len(set(stat_cat[z][1]))) + '\n   \n'
        z += 1
    return text


def stat_market_print():
    global stat_massive
    text = ''
    str1 = 'Название: '
    str2 = 'Всего кликов: '
    str3 = 'Уникальных пользователей: '
    print('stat_massive: ', stat_massive)
    print('len(stat_massive): ', len(stat_massive))
    for z in range(len(stat_massive)):
        if len(stat_massive[z][1]) > 0:
            text += str1 + stat_massive[z][0] + '\n'
            text += str2 + str(len(stat_massive[z][1])) + '\n'
            text += str3 + str(len(set(stat_massive[z][1]))) + '\n   \n'
    if text == '':
        text = 'Пока ещё не было посещений🤷🏻‍♂️'
    return text


bot: TeleBot = telebot.TeleBot(TOKEN)
gc = gspread.service_account(filename=GOOGLE_JSON)
link_to_table = TABLE_URL

sht2 = gc.open_by_url(link_to_table)
worksheet = sht2.sheet1
list_of_lists = worksheet.get_all_values()
len_lol = len(list_of_lists)

# Main menu
stat_cat = []
cat_main = []
for i in range(1, len_lol):
    cat_main.append(list_of_lists[i][8])
cat_main = set(cat_main)
markup_main = types.InlineKeyboardMarkup()
for n in cat_main:
    markup_main.add(types.InlineKeyboardButton(n, callback_data="1" + n))
    stat_cat.append([n, []])
markup_main.add(types.InlineKeyboardButton("Все скидки в таблице", url=link_to_table))

# Return_key
markup_return = types.InlineKeyboardMarkup()
markup_return.add(types.InlineKeyboardButton("Вернуться в меню", callback_data='3'))

stat_massive = []
mass_of_unic_markets = []
for i in range(1, len_lol):
    item = list_of_lists[i][0]
    unic_market = item.strip(' ')
    mass_of_unic_markets.append(unic_market)
mass_of_unic_markets = set(mass_of_unic_markets)

for j in mass_of_unic_markets:
    stat_massive.append([j, []])


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Выберите категорию в которой хотите получить скидку ⬇️",
                         reply_markup=markup_main)
    elif message.text == '/stat1':
        bot.send_message(message.chat.id, 'Статистика по категориям\n\n' + stat_cat_print(),
                         reply_markup=markup_return)
    elif message.text == '/stat2':
        bot.send_message(message.chat.id, 'Статистика по магазинам/сервисам.\n\n' + stat_market_print(),
                         reply_markup=markup_return)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id,)
    cat = f_cat(call.data)
    flag = f_flag(call.data)
    if flag == '1':
        bot.send_message(call.message.chat.id, "Выбирайте 🥰", reply_markup=keys_dynamic(cat, flag))
        stat_cat_add(cat, call.message.chat.id)
    elif flag == '2':
        cat = market(cat, call.message.chat.id)
        bot.send_message(call.message.chat.id, "Куда отправимся за скидками дальше?🥳",
                         reply_markup=keys_dynamic(cat, flag))
    elif flag == '3':
        bot.send_message(call.message.chat.id, "Выберите категорию в которой хотите получить скидку ⬇️",
                         reply_markup=markup_main)


print("Ready")
bot.infinity_polling()
