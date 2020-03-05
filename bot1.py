import aiohttp
import telebot
from telebot import types
import psycopg2
import config
import dbworker
import random

flag_reg_start = random.uniform(0, 100)

bot = telebot.TeleBot(config.token)

connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="123",
                              host="127.0.0.1",
                              port="5432")
cursor = connection.cursor()

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Аниме на аве', 'Вилку в глаз или не вилку в глаз ?')

KeyYN = telebot.types.ReplyKeyboardMarkup(True, True)
KeyYN.row('Да', 'Нет')

Keybivaet = telebot.types.ReplyKeyboardMarkup(True, True)
Keybivaet.row('Напишу правильно в следующем сообщении')

Keyreg = telebot.types.ReplyKeyboardMarkup(True, True)
Keyreg.row('/reg')

Keyok = telebot.types.ReplyKeyboardMarkup(True, True)
Keyok.row('Хорошо')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Я не Саня', 'Я сладкий пирожочек')

keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Участник', 'Организатор', 'Я булочка без начинки')

MenuPosv = telebot.types.ReplyKeyboardMarkup(True, True)
MenuPosv.row('Жилье', 'Карта', 'Ночные точки', 'Нужна мед помощь', 'Дестрой')

MenuKey = telebot.types.ReplyKeyboardMarkup(True, True)
MenuKey.row('Карта ', 'Расписание')

Menu = MenuKey

Key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
Key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboardinlineYN = telebot.types.InlineKeyboardMarkup()
keyboardinlineYN.add(Key_yes)
keyboardinlineYN.add(Key_no)

Kname = types.InlineKeyboardMarkup()
Name_button = types.InlineKeyboardButton(text='Ошибся в имени - тык сюда', callback_data='name')
Kname.add(Name_button)

Kmiddle = types.InlineKeyboardMarkup()
Name_button = types.InlineKeyboardButton(text='Ошибся в фамилии - тык сюда', callback_data='middle')
Kmiddle.add(Name_button)

Kfamily = types.InlineKeyboardMarkup()
Name_button = types.InlineKeyboardButton(text='Ошибся в отчестве - тык сюда', callback_data='family')
Kfamily.add(Name_button)

Kphone = types.ReplyKeyboardMarkup(True, True)
phone_button = types.KeyboardButton(text='Поделиться телефоном', request_contact=True)
Kphone.add(phone_button)

Kgroup = types.InlineKeyboardMarkup()
Name_button = types.InlineKeyboardButton(text='Ошибся в названии группы - тык сюда', callback_data='group')
Kgroup.add(Name_button)

Kdate = types.InlineKeyboardMarkup()
Name_button = types.InlineKeyboardButton(text='Ошибся в дате рождения - тык сюда', callback_data='date')
Kdate.add(Name_button)

Kvk = types.InlineKeyboardMarkup()
Name_button = types.InlineKeyboardButton(text='Ошибся в ссылке вк - тык сюда', callback_data='vk')
Kvk.add(Name_button)


@bot.message_handler(commands=['info'])
def text(msg):
    cursor.execute(
        '''select telegram_id from people p where exists(select * from spec s where p.p_id=s.spec_id and s.inform=1)''')
    rows_info = cursor.fetchall()
    for row in rows_info:
        if row[0] == msg.from_user.username:
            bot.send_message(msg.chat.id, 'Введи текст, который будет отправлен всем участникам')
            bot.register_next_step_handler(msg, info)
            break
        else:
            bot.send_message(msg.chat.id, 'Эээ, куда \n Недостаточно прав')


def info(msg):
    cursor.execute(''' select chat_id from people where work_status=2''')
    chat_id = cursor.fetchall()
    for i in chat_id:
        if msg.text != None:
            bot.send_message(i[0], msg.text)
        if msg.photo != None:
            a = msg.photo[-1].file_id
            bot.send_photo(i[0], a)


@bot.message_handler(commands=['help'])
def start_message1(msg):
    bot.send_message(msg.chat.id,
                     'Бот в процессе разработки.\nИдеи можно кидать сюда @ArmageddonReloaded')


@bot.message_handler(commands=['k'])
def start_message1(msg):
    bot.send_message(msg.chat.id,
                     'k')


# надо сделать пароль / либо только для избранных
def peopleshow(msg):
    cursor.execute("""select p_id,middle_name,first_name
           from people order by p_id""")
    rows = cursor.fetchall()
    for r in rows:
        bot.send_message(msg.chat.id, (f"  {r[0]}  {r[1]}  {r[2]}  "))


# вопрос юзеру по выбору роли
@bot.message_handler(commands=['start'])
# проверка по username и занесение в базу chat_id
# 0 - никто, 1 - орг, 2 - участник
def start_message(msg):
    if dbworker.get_state(msg.chat.id) == config.States.S_START.value or dbworker.get_state(
            msg.chat.id) == config.States.S_ENTER_RiGHT.value:

        user = msg.from_user.username

        cursor.execute("""select chat_id,p_id,work_status
          from people
           where telegram_id='%s'""" % (str(user)))
        rows = cursor.fetchall()

        if len(rows) > 0:
            if rows[0][2] == 0:

                photo = open('Who.jpg', 'rb')
                bot.send_photo(msg.chat.id, photo)

                bot.send_message(msg.chat.id,
                                 'Какая у тебя роль в событии ?\nВнимание! Этот пункт выбирается только один раз.\n',
                                 reply_markup=keyboard3)
                bot.register_next_step_handler(msg, login)

            else:
                bot.send_message(msg.chat.id,
                                 'Я же предупреждал. Уже не поменяешь :) \nНо если очень нужно, то пиши @ArmageddonReloaded')
        else:
            bot.send_message(msg.chat.id, 'You are not in base,\n enter the /reg.')


def login(msg):
    user = msg.from_user.username
    cursor.execute("""select chat_id,p_id,work_status
             from people
              where telegram_id='%s'""" % (str(user)))
    rows = cursor.fetchall()
    if rows[0][1] != None:
        bot.send_message(msg.chat.id, 'You are in base.\nПереход в основное меню', reply_markup=Menu)

        if msg.text != 'Я булочка без начинки' and rows[0][2] != 2:
            if msg.text == 'Организатор':
                cursor.execute(''' update people set work_status='%s' where telegram_id='%s' ''' % (
                    1, msg.from_user.username))
                connection.commit()
            else:
                cursor.execute(
                    ''' update people set work_status='%s' where telegram_id='%s' ''' % (
                        2, msg.from_user.username))
                connection.commit()
        if rows[0][0] == None:
            username = str(msg.from_user.username)
            cursor.execute(
                '''update people set chat_id=%s where telegram_id='%s' ''' % (int(msg.chat.id), username))
            connection.commit()


@bot.message_handler(commands=['reg'])
def start_message1(msg):
    cursor.execute(''' select *  from people where telegram_id='%s' ''' % (msg.from_user.username))
    rows = cursor.fetchall()
    dbworker.set_none(msg.chat.id)
    if len(rows) == 0:
        global flag_reg_start

        dbworker.set_var(msg.chat.id, 'flag_reg_start', flag_reg_start)

        dbworker.set_var(msg.chat.id, 'Username', msg.from_user.username)

        dbworker.set_var(msg.chat.id, 'Chatid', msg.chat.id)

        mes = bot.send_message(msg.chat.id,
                               'Попробуйте о себе что-нибудь вспомнить.\nНажимая "Хорошо", вы даете согласие на обработку персональных данных',
                               reply_markup=Keyok)

        dbworker.set_state(msg.chat.id, config.States.S_ENTER_NAME.value)

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        bot.send_message(msg.chat.id, 'Ты уже в базе')


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_NAME.value and isinstance(msg.text,
                                                                                                        str))
def name(msg):
    global flag_reg_start

    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, text=config.Questions.Name.value)
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_MIDDLE.value)

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_MIDDLE.value and isinstance(msg.text,
                                                                                                          str))
def Middle(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):

        dbworker.set_var(msg.chat.id, 'Name', msg.text)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Middle.value, reply_markup=Kname)

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_FAMILY.value)

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_FAMILY.value and isinstance(msg.text,
                                                                                                          str))
def Family(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):

        dbworker.set_var(msg.chat.id, 'Middle', msg.text)

        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        mes = bot.send_message(msg.chat.id, text=config.Questions.Family.value, reply_markup=Kmiddle)

        dbworker.set_state(msg.chat.id, config.States.S_ENTER_GROUP.value)

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_GROUP.value and isinstance(msg.text,
                                                                                                         str))
def Group(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):

        dbworker.set_var(msg.chat.id, 'Family', msg.text)

        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        mes = bot.send_message(msg.chat.id, text=config.Questions.Group.value, reply_markup=Kfamily)
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_PHONE.value)

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_PHONE.value and isinstance(msg.text,
                                                                                                         str))
def Phone(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))

        dbworker.set_var(msg.chat.id, 'Group', msg.text)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Phone.value, reply_markup=Kphone)

        dbworker.set_var(msg.chat.id, 'last_key_mes', mes.message_id)
        mes = bot.send_message(msg.chat.id, text=config.Questions.PhoneQ.value, reply_markup=Kgroup)

        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_DATE.value)

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(content_types=[
    'contact'])
def Bdate(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start') and dbworker.get_state(
            msg.chat.id) == config.States.S_ENTER_DATE.value:

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))
        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'last_key_mes'))

        if int(dbworker.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(dbworker.get_var(msg.chat.id, 'len')):
                bot.delete_message(msg.chat.id, int(dbworker.get_var(msg.chat.id, str(i))))
                i += 1
            dbworker.set_var(msg.chat.id, 'len', 0)

        dbworker.set_var(msg.chat.id, 'Phone', msg.contact.phone_number)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Date.value)

        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_VKURL.value)

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(content_types=['text'],
                     func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_DATE.value)
def wrong_phone(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, 'Нажми на кнопку в доп. клавиатуре')
        i = dbworker.get_var(msg.chat.id, 'len')
        dbworker.set_var(msg.chat.id, i, mes.message_id)
        dbworker.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        dbworker.set_var(msg.chat.id, 'len', str(int(i) + 2))

    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_VKURL.value and isinstance(msg.text,
                                                                                                         str) and dbworker.validate(
        msg.text))
def VKurl(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))

        # Date = msg.text
        dbworker.set_var(msg.chat.id, 'Date', msg.text)
        if int(dbworker.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(dbworker.get_var(msg.chat.id, 'len')):
                bot.delete_message(msg.chat.id, int(dbworker.get_var(msg.chat.id, str(i))))
                i += 1
            dbworker.set_var(msg.chat.id, 'len', 0)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Vk.value, reply_markup=Kdate)

        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_STOP.value)

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                         reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_VKURL.value and isinstance(msg.text,
                                                                                                         str) and not dbworker.validate(
        msg.text))
def wrong_date(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, 'Неправильный формат даты')
        i = dbworker.get_var(msg.chat.id, 'len')
        dbworker.set_var(msg.chat.id, str(i), mes.message_id)

        dbworker.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        dbworker.set_var(msg.chat.id, 'len', str(int(i) + 2))
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_STOP.value and isinstance(msg.text,
                                                                                                        str))
def last_message1(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):

        dbworker.set_var(msg.chat.id, 'VK', msg.text)
        if int(dbworker.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(dbworker.get_var(msg.chat.id, 'len')):
                bot.delete_message(msg.chat.id, int(dbworker.get_var(msg.chat.id, str(i))))
                i += 1
            dbworker.set_var(msg.chat.id, 'len', 0)

        bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))
        question = 'Тебя зовут ' + dbworker.get_var(msg.chat.id, 'Middle') + ' ' + dbworker.get_var(msg.chat.id,
                                                                                                    'Name') + ' ' + dbworker.get_var(
            msg.chat.id, 'Family') + '. Дата рождения' + dbworker.get_var(msg.chat.id,
                                                                          'Date') + '. Группа-' + dbworker.get_var(
            msg.chat.id, 'Group') + '. Номер телефона:' + dbworker.get_var(msg.chat.id,
                                                                           'Phone') + '. Ссылка на вк- ' + dbworker.get_var(
            msg.chat.id, 'VK') + '. Верно ?'
        mes = bot.send_message(msg.from_user.id, text=question, reply_markup=keyboardinlineYN)

        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_RiGHT)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    global flag_reg_start, rows
    if str(flag_reg_start) == dbworker.get_var(call.message.chat.id, 'flag_reg_start'):
        if call.data == "yes" and dbworker.get_var(call.message.chat.id, 'flag_stop') != 'False':
            dbworker.set_var(call.message.chat.id, 'flag_stop', 'True')
            bot.delete_message(call.message.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            cursor.execute(
                ''' insert into people (first_name, middle_name, family_name, group_name, phone, telegram_id,   birth_date, check_in, status, vk_url, chat_id, work_status) values('%s','%s','%s','%s',%s,'%s','%s',null,default ,'%s',%s,default)''' % (
                    dbworker.get_var(call.message.chat.id, 'Name'), dbworker.get_var(call.message.chat.id, 'Middle'),
                    dbworker.get_var(call.message.chat.id, 'Family'), dbworker.get_var(call.message.chat.id, 'Group'),
                    dbworker.get_var(call.message.chat.id, 'Phone'), dbworker.get_var(call.message.chat.id, 'Username'),
                    dbworker.get_var(call.message.chat.id, 'Date'), dbworker.get_var(call.message.chat.id, 'VK'),
                    dbworker.get_var(call.message.chat.id, 'Chatid')))
            connection.commit()
            bot.send_message(call.message.chat.id, text=config.Questions.Stop.value)
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_RiGHT.value)

            dbworker.set_none(call.message.chat.id)
        elif call.data == "no" and dbworker.get_var(call.message.chat.id, 'flag_stop') != 'True':
            dbworker.set_var(call.message.chat.id, 'flag_stop', 'False')
            bot.delete_message(call.message.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.send_message(call.message.chat.id, 'Хм. Придется снова пройти этап регистрации', reply_markup=Keyreg)

            dbworker.set_state(call.message.chat.id, config.States.S_START.value)
        elif call.data == 'name':
            mes = bot.send_message(call.message.chat.id, 'Ну как ты так, вроде имя - одно.\n А как правильно ?')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_MIDDLE.value)
        elif call.data == 'middle':
            mes = bot.send_message(call.message.chat.id, 'Ну как ты так, фамилию забыл.\n А как правильно ?')

            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_FAMILY.value)
        elif call.data == 'family':
            mes = bot.send_message(call.message.chat.id, 'Блен на тоби отец обидится.\n Какое у тебя отчество?')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_GROUP.value)
        elif call.data == 'group':
            mes = bot.send_message(call.message.chat.id, 'Тебя будут хейтить одногруппники.\n Какая группа ?')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'last_key_mes'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_PHONE.value)
        elif call.data == 'date':
            mes = bot.send_message(call.message.chat.id,
                                   'Подсказка - в этот день ты родился.\n Напиши, если вспомнил(а)')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_VKURL.value)
    else:
        dbworker.set_state(call.message.chat.id, config.States.S_START.value)
        bot.send_message(call.message.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                         reply_markup=Keyreg)


@bot.message_handler(content_types=['text'])
def send_text(msg):
    if 'Аниме на аве' in msg.text:
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
        photo = open('map.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Ночные точки' in msg.text:
        photo = open('play.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Расписание' in msg.text:
        photo = open('schedule.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Нужна мед помощь' in msg.text:
        photo = open('schedule.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
        # 'Дестрой')


bot.polling()
