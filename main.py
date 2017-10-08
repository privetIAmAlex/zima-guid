# -*- coding: UTF-8 -*-
import constants
import keyboards
import telebot
import sqlite3

bot = telebot.TeleBot(constants.TOKEN)
my_dict = dict()
admin_dict = dict()

@bot.message_handler(commands=["start"])
def handle_start(message):
    connection = sqlite3.connect(r"D:\My files\Бот guid\database.sqlite")
    cursor = connection.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM `cat`")
    c = count.fetchone()[0]
    ids = cursor.execute("INSERT INTO `users` ('telegram_id') VALUES ('{}')".format(message.chat.id))
    connection.commit()
    count_users = cursor.execute("SELECT COUNT(*) FROM `users`")
    cu = count_users.fetchone()[0]
    mess = "Количество организаций в базе данных: <b>{}</b>\nКоличество пользователей ботом: <b>{}</b>\nДобро пожаловать!".format(c + 11, cu + 11)
    bot.send_message(message.chat.id, mess, reply_markup=keyboards.started_keyboard, parse_mode="HTML")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    #------
    def template(category):
        my_dict.clear()
        connection = sqlite3.connect(r"D:\My files\Бот guid\database.sqlite")
        cursor = connection.cursor()
        orgs = cursor.execute("SELECT * FROM `cat` WHERE `category` = '{}'".format(category))
        c = orgs.fetchall()
        j = 0
        mess = ""
        for i in c:
            my_dict[j+1] = (i[3], i[0], i[2])
            mess += "{} - {}\n".format(j+1, i[3])
            j+=1
        bot.send_message(message.chat.id, mess)
        request = bot.send_message(message.chat.id, "Введите порядковый номер организации:")
        bot.register_next_step_handler(request, number_step)
    #-----

    if message.text == "Все организации":
        bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=keyboards.orgs_keyboard)
    elif message.text == "\u2B05\uFE0F На главную":
        bot.send_message(message.from_user.id, "Привет!\U0001f604", reply_markup=keyboards.started_keyboard)
#Template
    elif message.text == "Школы \U0001F3EB":
        template("school")
    elif message.text == "Кафе | Бары\U0001F374":
        template("cafe")
    elif message.text == "Больницы\U0001F3E5":
        template("hospital")
    elif message.text == "Парикмахерские\U0001F487":
        template("barbershop")
    elif message.text == "Такси\U0001F695":
        template("taxi")
    elif message.text == "Спортивные\U0001F3C0":
        template("sport")
    elif message.text == "Развлечения\U0001F3A4":
        template("enter")
    elif message.text == "Ремонт | Сервис\U0001F6E0":
        template("service")
    elif message.text == "Магазины\U0001F6CD":
        template("shop")
    elif message.text == "Компании\U0001F465":
        template("company")
    elif message.text == "Другие\u27A1\uFE0F":
        template("other")

#----------
    elif message.text == "Поиск по ID":
        request = bot.send_message(message.chat.id, "Введите ID:")
        bot.register_next_step_handler(request, search_by_id)
    elif message.text == "Другое":
        connection = sqlite3.connect(r"D:\My files\Бот guid\database.sqlite")
        cursor = connection.cursor()
        count = cursor.execute("SELECT COUNT(*) FROM `cat`")
        c = count.fetchone()[0]
        count_users = cursor.execute("SELECT COUNT(*) FROM `users`")
        cu = count_users.fetchone()[0]
        mess = "Количество организаций в базе данных: <b>{}</b>\nКоличество пользователей: <b>{}</b>\nПо всем вопросам: @alexes19".format(c + 11, cu + 11)
        bot.send_message(message.chat.id, mess, reply_markup=keyboards.other_keyboard, parse_mode="HTML")

    elif message.text == "add org in db hiked29hdknedf":
        bot.send_message(message.chat.id, "You have connected to the database")
        request = bot.send_message(message.chat.id, "Enter category name")
        bot.register_next_step_handler(request, category_name)
    
    elif message.text == "delete org from db hiked29hdknedf":
        request = bot.send_message(message.chat.id, "Enter id")
        bot.register_next_step_handler(request, delete_by_id)

    else:
        bot.send_message(message.chat.id, "Воспользуйтесь меню " + u"\u2935\uFE0F")
        
def delete_by_id(message):
    try:
        org_id = int(message.text)
        connection = sqlite3.connect(r"D:\My files\Бот guid\database.sqlite")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM `cat` WHERE `id` = '{}'".format(org_id))
        connection.commit()
        bot.send_message(message.chat.id, "Deleted({})".format(org_id))
    except Exception as e:
        bot.send_message(message.chat.id, "Error:\n" + str(e))

def number_step(message):
    try:
        num = message.text
        mess = "<b>{}</b>\nID: {}\n{}".format(my_dict[int(num)][0], my_dict[int(num)][1], my_dict[int(num)][2])
        bot.send_message(message.chat.id, mess, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, 'Повторите попытку позже.')
        
def search_by_id(message):
    try:
        connection = sqlite3.connect(r"D:\My files\Бот guid\database.sqlite")
        cursor = connection.cursor()
        id_obj = cursor.execute("SELECT * FROM `cat` WHERE `id` = '{}'".format(int(message.text)))
        c = id_obj.fetchall()
        response = "<b>{}</b>\nID: {}\n{}".format(c[0][3], c[0][0], c[0][2])
        bot.send_message(message.chat.id, response, parse_mode="HTML")
    except Exception as e:
        pass

def category_name(message):
    admin_dict["category"] = message.text
    request = bot.send_message(message.chat.id, "Enter title")
    bot.register_next_step_handler(request, title_name)
def title_name(message):
    admin_dict["title"] = message.text
    request = bot.send_message(message.chat.id, "Enter contacts")
    bot.register_next_step_handler(request, contacts)
def contacts(message):
    admin_dict["contacts"] = message.text
    request = bot.send_message(message.chat.id, "Result:\n" + str(admin_dict))
    bot.register_next_step_handler(request, commit_admin)
def commit_admin(message):
    if message.text == "yes":
        connection = sqlite3.connect(r"D:\My files\Бот guid\database.sqlite")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO `cat` ('category', 'contacts', 'title') VALUES ('{}', '{}', '{}')".format(admin_dict["category"], \
                                                                                                        admin_dict["contacts"], \
                                                                                                        admin_dict["title"]))
        connection.commit()
        bot.send_message(message.chat.id, "Added")
    else:
        admin_dict.clear()
        bot.send_message(message.chat.id, "Cleared")

bot.polling(none_stop=True)

#fetchone/fetchall
#print(c[1][0])