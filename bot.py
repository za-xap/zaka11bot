from datetime import datetime
from traceback import format_exc

import requests
import telebot
from bs4 import BeautifulSoup
from geopy.distance import geodesic
from telebot import types

import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def text(message):
    dtn = datetime.now()
    botlogfile = open('bot.log', 'a', encoding="utf-8")
    none = None
    if message.from_user.last_name is not none:
        print(dtn.strftime("%d-%m-%Y %H:%M:%S"), 'Юзер ' + message.from_user.first_name, message.from_user.last_name,
              "ID:", message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    elif message.from_user.last_name is none:
        print(dtn.strftime("%d-%m-%Y %H:%M:%S"), 'Юзер ' + message.from_user.first_name, "ID:", message.from_user.id,
              'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    try:
        if message.text == 'Привіт' or message.text == "test" or message.text == "Test" or message.text == "/start":
            none = None
            if message.from_user.last_name is not none:
                bot.send_message(message.from_user.id,
                                 "Привіт, {mention}!\nЯ <b>{1.first_name}</b>, подивись мої команди.".format(
                                     message.from_user, bot.get_me(),
                                     mention=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name} {message.from_user.last_name}</a>'),
                                 parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
                try:
                    file = open("user.log")
                except IOError:
                    file = open("user.log", "w", encoding="utf-8")
                    file.close()
                    file = open("user.log")
                string = file.read()
                search_word = str(message.from_user.id)
                if search_word in string:
                    file.close()
                else:
                    dtn = datetime.now()
                    userlogfile = open('user.log', 'a')
                    print(dtn.strftime("%d-%m-%Y %H:%M:%S"), "ID:", message.from_user.id, "username:",
                          message.from_user.username, "Name:", message.from_user.first_name,
                          message.from_user.last_name, file=userlogfile)
                    userlogfile.close()
            elif message.from_user.last_name is none:
                bot.send_message(message.from_user.id,
                                 "Привіт, {mention}!\nЯ <b>{1.first_name}</b>, подивись мої команди.".format(
                                     message.from_user, bot.get_me(),
                                     mention=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'),
                                 parse_mode="HTML")
                file = open("user.log")
                string = file.read()
                search_word = str(message.from_user.id)
                if search_word in string:
                    file.close()
                else:
                    dtn = datetime.now()
                    userlogfile = open('user.log', 'a')
                    print(dtn.strftime("%d-%m-%Y %H:%M:%S"), "ID:", message.from_user.id, "username:",
                          message.from_user.username, "Name:", message.from_user.first_name, file=userlogfile)
                    userlogfile.close()
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши привіт")
        elif message.text == "go" or message.text == "Go":
            bot.send_message(message.from_user.id, 'Go, go, go!')
        elif message.text == "H" or message.text == "h" or message.text == "/h":
            url = 'https://steamcommunity.com/id/Za_XaP'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features="lxml")
            i = soup.find("div", {"class": "game_info_details"}).get_text()
            i = i.split("\r\n\t\t\t\t\t\t\t\t\t\t\t")
            i = i[1].split(" ")
            i = i[0]
            if "," in i:
                i = i.replace(",", "")
            bot.send_message(message.from_user.id, "Admin has {} hours in the last game".format(i))
        elif message.text == "/time" or message.text == "time":
            now = datetime.now()
            bot.send_message(message.from_user.id, "UTC - " + now.strftime("%H:%M:%S"),
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "/id" or message.text == "Id":
            bot.send_message(message.from_user.id,
                             "Ваш телеграм ID - <code>{ID}</code>".format(ID=message.from_user.id), parse_mode="HTML",
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "/toadm":
            bot.send_message(message.from_user.id, 'Введіть /toadm текст')
        elif message.text.startswith("/toadm"):
            if not message.text.startswith("/toadm "):
                bot.send_message(message.from_user.id, 'Введіть /toadm текст')
            else:
                x = message.text.split(' ', 1)
                try:
                    bot.send_message(message.from_user.id, "Повідомлення відправлено адміну бота!")
                    bot.send_message(550557267, "Повідомлення від {mention}:\n\n{msg}".format(
                        mention=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name} {message.from_user.last_name}</a>',
                        msg=x[1]), parse_mode="HTML")
                    bot.forward_message(550557267, message.from_user.id, message.message_id)
                except BaseException:
                    bot.send_message(message.from_user.id, 'Введіть /toadm текст')
        elif message.text.startswith("/touser") and message.from_user.id == 550557267:
            if not message.text.startswith("/touser "):
                bot.send_message(message.from_user.id, 'Введіть /touser ID текст')
            else:
                x = message.text.split(' ', 2)
                try:
                    iduser = int(x[1])
                    bot.send_message(message.from_user.id, "Повідомлення відправлено юзеру!")
                    bot.send_message(iduser, "Повідомлення від адміна:\n\n{msg}".format(msg=x[2]), parse_mode="HTML")
                except BaseException:
                    bot.send_message(message.from_user.id, 'Введіть /touser ID текст')
        elif message.text == "/whereadm":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            button = types.KeyboardButton(text='Відправити розташування', request_location=True)
            markup.add(button)
            bot.send_message(message.from_user.id, 'Відправ своє розташування, та я скажу як далеко адмін!',
                             reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, "Я тебя не розумію. Напиши /help.",
                             reply_markup=types.ReplyKeyboardRemove())
    except BaseException:
        bot.send_message(message.from_user.id,
                         "ERROR! Щось пішло не так...\nЯкщо ви бачите це повідомлення, повідомте про проблему {}! Скажіть, яке повідомленяя викликало це повідомлення.".format(
                             '<a href="tg://user?id=550557267">адміна</a>'), parse_mode="HTML")
        bot.send_message(550557267, "ID: " + str(message.from_user.id) + " Text: " + message.text + "\n" + format_exc())


@bot.message_handler(content_types=['location'])
def location(message):
    try:
        if message.location is not None:
            adm = (50.05920, 36.28530)
            us = (message.location.latitude, message.location.longitude)
            bot.send_message(message.from_user.id, "Адмін знаходиться від цієї точки в {d} кілометрах".format(
                d=round(geodesic(adm, us).km, 1)), parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
    except BaseException:
        bot.send_message(message.from_user.id,
                         "ERROR! Щось пішло не так...\nЯкщо ви бачите це повідомлення, повідомте про проблему {}! "
                         "Скажіть, яке повідомленяя викликало це повідомлення.".format(
                             '<a href="tg://user?id=550557267">адміна</a>'), parse_mode="HTML")
        bot.send_message(550557267, "ID: " + str(message.from_user.id) + " LOCATION" + "\n" + format_exc())
    dtn = datetime.now()
    botlogfile = open('bot.log', 'a', encoding="utf-8")
    none = None
    if message.from_user.last_name is not none:
        print(dtn.strftime("%d-%m-%Y %H:%M:%S"), 'Юзер ' + message.from_user.first_name, message.from_user.last_name,
              "ID:", message.from_user.id, 'прислал точку: ' + str(message.location.latitude),
              str(message.location.longitude), file=botlogfile)
    elif message.from_user.last_name is none:
        print(dtn.strftime("%d-%m-%Y %H:%M:%S"), 'Юзер ' + message.from_user.first_name, "ID:", message.from_user.id,
              'прислал точку: ' + str(message.location.latitude), str(message.location.longitude), file=botlogfile)
    botlogfile.close()


bot.polling(none_stop=True, interval=0)
