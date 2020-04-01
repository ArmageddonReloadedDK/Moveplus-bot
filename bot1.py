import time
import telebot
from telebot import types
import psycopg2
import config
import dbworker
import random
import datetime
import functions as func
from PIL import Image
from telebot import apihelper

# apihelper.proxy={"https":"socks5://198.199.120.1002:1080"}

flag_reg_start = random.uniform(0, 20)

bot = telebot.TeleBot(config.token)

connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="123",
                              host="localhost",
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

leave_yes_not = types.InlineKeyboardMarkup()
leave_yes_button = types.InlineKeyboardButton(text='Да', callback_data='leave_yes')
leave_not_button = types.InlineKeyboardButton(text='Нет', callback_data='leave_not')
leave_yes_not.add(leave_yes_button)
leave_yes_not.add(leave_not_button)

accept_reject = types.InlineKeyboardMarkup()
accept = types.InlineKeyboardButton(text='Принять', callback_data='accept')
reject = types.InlineKeyboardButton(text='Отклонить', callback_data='reject')
accept_reject.add(accept)
accept_reject.add(reject)


key = types.InlineKeyboardMarkup()
key_button = types.InlineKeyboardButton(text='Есть ключ', callback_data='key')
key_no_button = types.InlineKeyboardButton(text='Нет ключа', callback_data='no_key')
key.add(key_button)
key.add(key_no_button)


@bot.message_handler(commands=['regchange'])
def chang1(msg):
    if func.type(msg, 1):
        if not func.reg_type(msg) or func.reg_type(msg) is None:
            cursor.execute(''' update people set regist=True where chat_id='%s' ''' % (msg.chat.id))
            connection.commit()
            bot.send_message(msg.chat.id, 'Статус изменен на True ')

        else:
            cursor.execute(''' update people set regist=False where chat_id='%s' ''' % (msg.chat.id))
            connection.commit()
            bot.send_message(msg.chat.id, 'Статус изменен на False ')
    else:
        func.no_permis(msg)


@bot.message_handler(commands=['change'])
def chang1(msg):
    if func.here(msg):
        bot.send_message(msg.chat.id, 'Введи номер человека, у которого нужно сменить статус')
        bot.register_next_step_handler(msg, chang2)
    else:
        func.no_permis(msg)


def chang2(msg):
    try:
        a = int(msg.text)
        cursor.execute(''' select p.chat_id from people p where p.p_id='%s' ''' % (int(msg.text)))
        rows = cursor.fetchall()
        if rows[0][0] == config.admin.Dav.value:
            bot.send_message(msg.chat.id, 'Сейчас бы главному админу менять статус')
        else:
            cursor.execute(''' select * from spec s where s.spec_id='%s' ''' % (a))
            rows = cursor.fetchall()
            if len(rows) > 0:
                bot.send_message(msg.chat.id, 'Какой статус ? True-1/False-0')
                bot.register_next_step_handler(msg, chang3)
                dbworker.set_var(msg.chat.id, 'cname', msg.text)
            else:
                bot.send_message(msg.chat.id, 'такого человека нет')
    except Exception:
        bot.send_message(msg.chat.id, 'ошибка в номере')


def chang3(msg):
    if '1' in msg.text:
        cursor.execute(
            ''' update spec set inform=TRUE where spec_id='%s' ''' % (dbworker.get_var(msg.chat.id, 'cname')))
        connection.commit()
        bot.send_message(msg.chat.id, 'Статус обвнолен. Для выведения списка спец лиц введите /list')
    elif '0' in msg.text:
        cursor.execute(
            ''' update spec set inform=FALSE where spec_id='%s' ''' % (dbworker.get_var(msg.chat.id, 'cname')))
        connection.commit()
        bot.send_message(msg.chat.id, 'Статус обвнолен. Для выведения списка спец лиц введите /list')


@bot.message_handler(commands=['leave'])
def leave1(msg):
    if func.type(msg, 1):
        bot.send_message(msg.chat.id, 'Куда ты собрался выселяться. Ты орг')
    else:
        cursor.execute(''' select l.state  from leave l  where l.participant_chat_id='%s' ''' % (msg.chat.id))
        rows = cursor.fetchall()
        if len(rows) > 0:
            if not rows[0][0]:
                bot.send_message(msg.chat.id, 'Заявка уже отправлена. Пожалуйста, ожидайте')
            elif rows[0][0]:
                bot.send_message(msg.chat.id, 'Вы уже покинули мероприятие :)')
        else:
            mes = bot.send_message(msg.chat.id, 'Насколько я понимаю, Вы хотите покинуть мероприятие.')
            mes1 = bot.send_message(msg.chat.id, ' Подтверждаете заявку?', reply_markup=leave_yes_not)
            dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
            dbworker.set_var(msg.chat.id, 'mes_to_del2', mes1.message_id)
            if dbworker.get_var(msg.chat.id, 'mes_to_del3')!=mes.message_id:
                bot.delete_message(msg.chat.id,int(dbworker.get_var(msg.chat.id, 'mes_to_del3')))
                bot.delete_message(msg.chat.id,int(dbworker.get_var(msg.chat.id, 'mes_to_del4')))
            dbworker.set_var(msg.chat.id, 'mes_to_del3', mes.message_id)
            dbworker.set_var(msg.chat.id, 'mes_to_del4', mes1.message_id)
            dbworker.set_state(msg.chat.id, config.States.S_START.value)
            dbworker.set_var(msg.chat.id, 'leave_yes', '0')
         #   dbworker.set_var(msg.chat.id, 'taken', '0')
         #   dbworker.set_var(msg.chat.id, 'key', '0')
         #   dbworker.set_var(msg.chat.id, 'accept', '0')


@bot.message_handler(commands=['info'])
def text(msg):
    if func.here(msg):
        bot.send_message(msg.chat.id, 'Введи текст, который будет отправлен всем участникам')
        bot.register_next_step_handler(msg, info)
    else:
        func.no_permis(msg)


def info(msg):
    cursor.execute(''' select chat_id from people where work_status=2''')
    chat_id = cursor.fetchall()
    for i in chat_id:
        if msg.text != None:
            bot.send_message(i[0], msg.text)
        if msg.photo != None:
            a = msg.photo[-1].file_id
            bot.send_photo(i[0], a)


@bot.message_handler(commands=['add'])
def add(msg):
    if func.here(msg):
        bot.send_message(msg.chat.id, 'Введите номер человека, которого нужно добавить ')
        bot.register_next_step_handler(msg, add2)
    else:
        func.no_permis(msg)


def add2(msg):
    try:
        a = int(msg.text)
        cursor.execute(''' select p.p_id from people p where p.p_id='%s' ''' % (a))
        rows = cursor.fetchall()
        if len(rows) > 0:

            cursor.execute('''insert into spec values('%s',0,TRUE)''' % (a))
            connection.commit()
            bot.send_message(msg.chat.id, 'Добавлено')
        else:
            bot.send_message(msg.chat.id, 'такого человека нет')
    except Exception:
        bot.send_message(msg.chat.id, 'ошибка в номере')


@bot.message_handler(commands=['family'])
def add(msg):
    if func.here(msg):
        bot.send_message(msg.chat.id, 'Введите фамилию человека, которого нужно найти ')
        bot.register_next_step_handler(msg, add2)
    else:
        func.no_permis(msg)


def add2(msg):
    try:
        a = str(msg.text)
        a.capitalize()
        cursor.execute(
            ''' select p.p_id,p.middle_name,p.first_name,p.family_name,p.phone,p.status,p.room_num from people p where p.middle_name='%s' ''' % (
                a))
        rows = cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                bot.send_message(msg.chat.id,
                                 f' Личный номер: {row[0]}\n{row[1]} {row[2]} {row[3]} \nНомер телефона: {row[4]}\nСтатус: {row[5]}\nНомер комнаты: {row[6]}')
        else:
            bot.send_message(msg.chat.id, 'такого человека нет')
    except Exception:
        bot.send_message(msg.chat.id, 'ошибка в фамимлии')


@bot.message_handler(commands=['help'])
def start_message1(msg):
    if func.type(msg, 1):
        bot.send_message(msg.chat.id,
                         'Бот в процессе разработки.Доступные команды: \n/list - список модераторов\n/add - добавить модератора\n'
                         '/change - изменить статус модератора\n/family - поиск людей по фамилии\n'
                         '/info - написать сообщение всем участникам\n/write - написать конкретному человеку\n'
                         '/count - количество людей в базе\n/regchange - готов/не готов выселять людей \nЗаметил косяк ? Пиши сюда @ArmageddonReloaded')
    else:
        bot.send_message(msg.chat.id,
                         'Бот в процессе разработки.Доступные команды: \n/start - начать процесс регистрации на мероприятии'
                         '\n/leave - подать заявку на выселение\nЗаметил косяк ? Пиши сюда @ArmageddonReloaded')


@bot.message_handler(commands=['write'])
def start_message1(msg):
    if func.here(msg):
        bot.send_message(msg.chat.id, 'Введи номер человека, кому нужно написать ')
        bot.register_next_step_handler(msg, num)
    else:
        func.no_permis(msg)


def num(msg):
    dbworker.set_var(msg.chat.id, 'pwrite', msg.text)
    bot.send_message(msg.chat.id, 'Что написать ему ?')
    bot.register_next_step_handler(msg, mes)


def mes(msg):
    try:
        a = int(dbworker.get_var(msg.chat.id, 'pwrite'))
        cursor.execute(''' select chat_id from people p where p_id='%s' ''' % (a))
        rows = cursor.fetchall()
        if len(rows) > 0:
            bot.send_message(rows[0][0], msg.text)
            bot.send_message(msg.chat.id, 'Доставлено')
        else:
            bot.send_message(msg.chat.id, ' Такого человека нет')
    except Exception:
        bot.send_message(msg.chat.id, ' Такого человека нет')


@bot.message_handler(commands=['list'])
def peopleshow(msg):
    if func.here(msg):
        cursor.execute("""select p.first_name,p.middle_name,s.inform from spec s,people p where p.p_id=s.spec_id""")
        rows = cursor.fetchall()
        for r in rows:
            bot.send_message(msg.chat.id, (f"  {r[1]}  {r[0]}  наличие доступа: {r[2]}  "))
    else:
        func.no_permis(msg)


@bot.message_handler(commands=['count'])
def peopleshow(msg):
    if func.here(msg):
        cursor.execute("""select count(*) from people """)
        rows = cursor.fetchall()
        for r in rows:
            bot.send_message(msg.chat.id, (f"  {r[0]}   "))
    else:
        func.no_permis(msg)


# вопрос юзеру по выбору роли
@bot.message_handler(commands=['start'])
# проверка по username и занесение в базу chat_id
# 0 - никто, 1 - орг, 2 - участник
def start_message(msg):
    if dbworker.get_state(msg.chat.id) == config.States.S_START.value or dbworker.get_state(
            msg.chat.id) == config.States.S_ENTER_RiGHT.value or dbworker.get_state(
        msg.chat.id) is None:

        cursor.execute("""select p_id,work_status from people where chat_id='%s' """ % (msg.chat.id))
        rows = cursor.fetchall()

        if len(rows) > 0:
            if rows[0][1] == 0:

                photo = open('Who.jpg', 'rb')
                bot.send_photo(msg.chat.id, photo)

                bot.send_message(msg.chat.id,
                                 'Какая у тебя роль в событии ?\nВнимание! Этот пункт выбирается только один раз.\n',
                                 reply_markup=keyboard3)
                bot.register_next_step_handler(msg, login)

            else:
                bot.send_message(msg.chat.id,
                                 'Я же предупреждал. Уже не поменяешь :) \nНо если очень нужно, то пиши @ArmageddonReloaded',
                                 reply_markup=Menu)
        else:
            bot.send_message(msg.chat.id, 'Тебя еще нет в базе,\nвведи /reg.')


def login(msg):
    cursor.execute("""select p_id,work_status from people where chat_id='%s'""" % (msg.chat.id))
    rows = cursor.fetchall()
    if rows[0][0] != None:
        bot.send_message(msg.chat.id, 'You are in base.\nПереход в основное меню', reply_markup=Menu)

        if msg.text != 'Я булочка без начинки' and rows[0][1] != 2:
            if msg.text == 'Организатор':
                cursor.execute(''' update people set work_status='%s' where chat_id='%s' ''' % (
                    1, msg.chat.id))
                connection.commit()
            else:
                cursor.execute(
                    ''' update people set work_status='%s' where chat_id='%s' ''' % (
                        2, msg.chat.id))
                connection.commit()


@bot.message_handler(commands=['reg'])
def start_message1(msg):
    cursor.execute(''' select *  from people where chat_id='%s' ''' % (msg.chat.id))
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
        question = 'Вас зовут ' + dbworker.get_var(msg.chat.id, 'Middle') + ' ' + dbworker.get_var(msg.chat.id,
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
    global flag_reg_start
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
            dbworker.set_state(call.message.chat.id, config.States.S_START.value)
            dbworker.set_var(call.message.chat.id, 'flag_stop', 'False')
            bot.delete_message(call.message.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.send_message(call.message.chat.id, 'Хм. Придется снова пройти этап регистрации', reply_markup=Keyreg)
        elif call.data == 'name' and dbworker.get_state(call.message.chat.id) != config.States.S_ENTER_MIDDLE.value:
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_MIDDLE.value)
            mes = bot.send_message(call.message.chat.id, 'Ну как ты так, вроде имя - одно.\n А как правильно ?')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'middle' and dbworker.get_state(call.message.chat.id) != config.States.S_ENTER_FAMILY.value:
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_FAMILY.value)
            mes = bot.send_message(call.message.chat.id, 'Ну как ты так, фамилию забыл.\n А как правильно ?')

            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'family' and dbworker.get_state(call.message.chat.id) != config.States.S_ENTER_GROUP.value:
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_GROUP.value)
            mes = bot.send_message(call.message.chat.id, 'Блен на тоби отец обидится.\n Какое у тебя отчество?')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'group' and dbworker.get_state(call.message.chat.id) != config.States.S_ENTER_PHONE.value:
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_PHONE.value)
            mes = bot.send_message(call.message.chat.id, 'Тебя будут хейтить одногруппники.\n Какая группа ?')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'last_key_mes'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)

        elif call.data == 'date' and dbworker.get_state(call.message.chat.id) != config.States.S_ENTER_VKURL.value:
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_VKURL.value)
            mes = bot.send_message(call.message.chat.id,
                                   'Подсказка - в этот день ты родился.\n Напиши, если вспомнил(а)')
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'user_wrong'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)

    if call.data == 'leave_yes' and dbworker.get_var(call.message.chat.id,'leave_yes')!='1':
        dbworker.set_var(call.message.chat.id, 'leave_yes','1')
        mes = bot.send_message(call.message.chat.id,
                               'Заявка принята. В течение 1-5 минут к Вашей комнате подойдет организатор. Пожалуйста, не уходите далеко от своего номера.')
        if dbworker.get_var(call.message.chat.id, 'mes_to_del') != 0:
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del2'))
        dbworker.set_var(call.message.chat.id, 'mes_to_del', 0)
        dbworker.set_var(call.message.chat.id, 'mes_to_del2', 0)
        cursor.execute(''' insert into leave( participant_chat_id) values('%s')''' % (call.message.chat.id))
        cursor.execute('''update leave set participant_id=(select p.p_id from people p where p.chat_id='%s') 
            where participant_chat_id='%s' ''' % (call.message.chat.id, call.message.chat.id))
        connection.commit()
        cursor.execute(''' select p.chat_id from people p where regist=true''')
        rows = cursor.fetchall()
        cursor.execute('''select p.p_id from people p where chat_id='%d' ''' % (call.message.chat.id))
        pid = cursor.fetchall()
        accept = types.InlineKeyboardMarkup()
        accept_button = types.InlineKeyboardButton(text='Принять заявку', callback_data='taken'+str(call.message.chat.id))
        accept.add(accept_button)
        for row in rows:
            mes = bot.send_message(row[0], 'Человек под номером %d хочет выселиться. ' % (pid[0][0]),
                                   reply_markup=accept)
            cursor.execute(
                ''' insert into msg_delivery( participant_chat_id, organizer_chat_id, msg_id, time) VALUES('%d','%d','%d','%s') ''' % (
                    call.message.chat.id, row[0], mes.message_id,datetime.datetime.now().strftime("%H:%M:%S")))
            connection.commit()

    elif call.data == 'leave_not' and dbworker.get_var(call.message.chat.id,'leave_not')!='1':
        dbworker.set_var(call.message.chat.id, 'leave_not','1')
        mes = bot.send_message(call.message.chat.id, 'Заявка отклонена.')
        if dbworker.get_var(call.message.chat.id, 'mes_to_del') != 0:
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
            bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del2'))
        dbworker.set_var(call.message.chat.id, 'mes_to_del', 0)
        dbworker.set_var(call.message.chat.id, 'mes_to_del2', 0)
        dbworker.set_state(call.message.chat.id, config.States.S_START.value)
        dbworker.set_var(call.message.chat.id, 'leave_not', '0')

    elif  'taken' in call.data and dbworker.get_var(call.message.chat.id,'taken')!='1':
        dbworker.set_var(call.message.chat.id, 'taken','1')
        cursor.execute(
            ''' select m.organizer_chat_id,msg_id,l.participant_id from msg_delivery m,leave l where m.participant_chat_id=l.participant_chat_id and m.state=true and l.participant_chat_id='%s' ''' % (
                call.data[5:len(call.data):1]))
        rows = cursor.fetchall()
        for row in rows:
            bot.delete_message(row[0], row[1])
        cursor.execute(''' update msg_delivery set state=False where participant_chat_id='%s' '''%(rows[0][2]))
        connection.commit()
        mes = bot.send_message(call.message.chat.id, 'Выселить человека под номером %s ?'%(rows[0][2]), reply_markup=accept_reject)
        dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        dbworker.set_var(call.message.chat.id, 'member', call.data[5:len(call.data):1])
        dbworker.set_var(call.message.chat.id, 'memberid', rows[0][2])
    elif call.data == 'accept' and dbworker.get_var(call.message.chat.id,'accept')!='1':
        dbworker.set_var(call.message.chat.id, 'accept','1')
        dbworker.set_state(int(dbworker.get_var(call.message.chat.id, 'member')), config.States.S_START.value)
    #    print(dbworker.get_var(call.message.chat.id, 'member'))
        mes = bot.send_message(call.message.chat.id, ' Есть ли у него ключ от номера ?', reply_markup=key)
     #   print(dbworker.get_state(call.message.chat.id))
        bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
        dbworker.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        cursor.execute(
            ''' update leave set state=True,check_out='%s' where participant_chat_id='%s' ''' % (
                datetime.datetime.now().strftime("%H:%M:%S"), dbworker.get_var(call.message.chat.id, 'member')))
        connection.commit()
    elif call.data == 'reject' and dbworker.get_var(call.message.chat.id,'reject')!='1':
        dbworker.set_var(call.message.chat.id, 'reject','1')
        dbworker.set_var(call.message.chat.id, 'taken', '0')
        dbworker.set_var(call.message.chat.id, 'accept', '0')
        dbworker.set_var(dbworker.get_var(call.message.chat.id, 'member'), 'leave_yes', '0')

        dbworker.set_state((call.message.chat.id, 'member'), config.States.S_START.value)
        bot.send_message(int(dbworker.get_var(call.message.chat.id, 'member')),
                         'Отказано в выселении.')
        mes = bot.send_message(call.message.chat.id,
                               '%s-му отказано в выселении.' % (dbworker.get_var(call.message.chat.id, 'memberid')))
        bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
        cursor.execute(''' delete from leave where participant_chat_id='%s' ''' % (
            dbworker.get_var(call.message.chat.id, 'member')))
        cursor.execute(''' delete from msg_delivery where participant_chat_id='%s' ''' % (
            dbworker.get_var(call.message.chat.id, 'member')))
        connection.commit()
        dbworker.set_var(call.message.chat.id, 'reject', '0')

    elif call.data == 'key' and dbworker.get_var(call.message.chat.id,'key')!='1':
        dbworker.set_var(call.message.chat.id, 'key','1')
        dbworker.set_var(call.message.chat.id, 'taken','0')
        dbworker.set_var(call.message.chat.id, 'accept','0')
        dbworker.set_var(dbworker.get_var(call.message.chat.id, 'member'), 'leave_yes','0')

        mes = bot.send_message(call.message.chat.id,
                               '%s-мой выселен.' % (dbworker.get_var(call.message.chat.id, 'memberid')))
        bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
        cursor.execute(
            ''' update leave set key=True where participant_chat_id='%s' ''' % (
                dbworker.get_var(call.message.chat.id, 'member')))
        cursor.execute(''' update msg_delivery set state=False where participant_chat_id='%s' ''' % (
            dbworker.get_var(call.message.chat.id, 'member')))
        connection.commit()
        bot.send_message(dbworker.get_var(call.message.chat.id, 'member'),'Подойдите к стойке регистрации. Вас будут там ожидать.')
        dbworker.set_var(call.message.chat.id, 'key', '0')

    elif call.data == 'no_key' and dbworker.get_var(call.message.chat.id,'no_key')!='1':
        dbworker.set_var(call.message.chat.id, 'no_key','1')
        dbworker.set_var(call.message.chat.id, 'taken', '0')
        dbworker.set_var(call.message.chat.id, 'accept', '0')
        dbworker.set_var(call.message.chat.id, 'leave_yes', '0')

        mes = bot.send_message(call.message.chat.id,
                               'чеовек с номером %s выселен.' % (dbworker.get_var(call.message.chat.id, 'memberid')))
        bot.send_message(dbworker.get_var(call.message.chat.id, 'member'),
                        'Подойдите к стойке регистрации. Вас будут там ожидать.')
        bot.delete_message(mes.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
    #   cursor.execute(
    #        ''' update leave set state=False where participant_chat_id=(select m.participant_chat_id from msg_delivery m where m.organizer_chat_id='%s')''' % (call.message.chat.id))
        cursor.execute(''' update msg_delivery set state=False where participant_chat_id='%s' ''' % (
            dbworker.get_var(call.message.chat.id, 'member')))
        connection.commit()
        dbworker.set_var(call.message.chat.id, 'no_key', '0')

    elif dbworker.get_state(call.message.chat.id) != config.States.S_busy.value and dbworker.get_state(
            call.message.chat.id) != config.States.S_not_busy.value and dbworker.get_state(
        call.message.chat.id) != config.States.S_START.value and dbworker.get_state(
        call.message.chat.id) != config.States.S_busy_org.value:
        bot.send_message(call.message.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                         reply_markup=Keyreg)
   # print(call.data)
   # print(dbworker.get_var(call.message.chat.id,'taken'))
   # print(call.data[4:len(call.data):1])



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
    else:
        bot.send_message(msg.chat.id, 'Нужен набор доступных команд ?Держи: ')

        # 'Дестрой')


bot.polling()
