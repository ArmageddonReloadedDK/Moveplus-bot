import telebot
from settings.config import token
from base.base_human import Base_human_class
import psycopg2
import datetime
from base.human import Human_class
import numpy as np

############################################
#
# Создание клавиатур
#
Menu = telebot.types.ReplyKeyboardMarkup(True, True)
Menu.row('Карта ', 'Расписание')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Аниме на аве', 'Вилку в глаз или не вилку в глаз ?')
#
#############################################

bot = telebot.TeleBot(token)
connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()
human = Human_class()


def num():
    yield


def find(msg):
    text = str(msg.text)
    text.capitalize()
    data = text.split(' ')
    if len(data) == 2:
        cursor.execute(
            ''' select p.p_id,p.family_name,p.first_name,p.middle_name,p.phone,p.group_name,r.room
                from ev_people p left join participants r on p.p_id = r.part_id
                where (select similarity(p.family_name,'%s'))>0.27 and (select similarity(p.first_name,'%s'))>0.27  ''' % (
                data[0], data[1]))
    else:
        bot.send_message(msg.chat.id, 'Нужны фамилия и имя')
    rows = cursor.fetchall()
    return rows


def regStatus(msg, bool):
    cursor.execute(
        ''' select p.p_id
            from ev_people p,organizators o
            where o.org_id=p.p_id and p.chat_id='%s' and o.regist='%s'  ''' % (
            msg.chat.id, bool))
    rows = cursor.fetchall()
    if rows:
        return True
    else:
        return False


def main_text_handler(msg):
    #
    # простой обработчик текстовых сообщений
    #

    if 'Аниме на аве' in msg.text:
        bot.send_message(msg.chat.id, 'Здоровья маме')
    if human.work_type(msg, 1):
        if regStatus(msg, True):
            data = find(msg)
            if len(data) == 1:
                cursor.execute(''' update ev_people p set time='%s'  where p_id='%s' 
                ''' % (str(datetime.datetime.now().strftime("%H:%M:%S")), data[0][0]))
                connection.commit()
                cursor.execute(''' select chat_id 
                                from ev_people p, organizators o 
                                where o.check_out is true and o.org_id=p.p_id
                            ''')
                orgs = cursor.fetchall()
                if len(orgs) != 1:
                    iter = np.random.randint(0, len(orgs))
                else:
                    iter = 0
                for row in data:
                    bot.send_message(msg.chat.id,
                                     f' Go.Отправлен на стойку регистрации: {iter}\n Личный номер:  {row[0]}\n{row[1]} {row[2]} {row[3]} '
                                     f'\nНомер телефона: {row[4]}\nГруппа {row[5]}\nНомер комнаты: {row[6]}')

                for row in data:
                    bot.send_message(orgs[iter][0],
                                     f'Стойка регистрации: {iter}\nОтправлен человек\n Личный номер:  {row[0]}\n{row[1]} {row[2]} {row[3]} '
                                     f'\nНомер телефона: {row[4]}\nГруппа {row[5]}\nНомер комнаты: {row[6]}')
            elif len(data) == 0:
                bot.send_message(msg.chat.id, 'Человек не найден')
            else:
                bot.send_message(msg.chat.id, 'Найдено больше одного человека\nВведи фамилию и имя точнее')


"""    if 'Аниме на аве' in msg.text:
        bot.send_message(msg.chat.id, 'Здоровья маме')

    elif 'Вилку в глаз или не вилку в глаз ?' in msg.text:
        bot.send_message(msg.chat.id, 'Я смотрю, ты не одноглазый')

    elif 'Я сладкий пирожочек' in msg.text:
        bot.send_message(msg.chat.id, 'Ну ладно, тебе прощаю')

    elif 'Я не Саня' in msg.text:
        bot.send_message(msg.chat.id, 'А кто тогда Саня, Я ? Жду сотку', reply_markup=keyboard1)
    elif 'Жилье' in msg.text:
        bot.send_message(msg.chat.id, 'Жилье')
    elif 'Карта' in msg.text:
        photo = open('images/map.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Ночные точки' in msg.text:
        photo = open('images/play.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Расписание' in msg.text:
        photo = open('images/schedule.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Нужна мед помощь' in msg.text:
        photo = open('images/schedule.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    else:
        bot.send_message(msg.chat.id, 'Нужен набор доступных команд ?Держи: ')"""
