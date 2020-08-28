import telebot
from telebot import types
from settings import config
from database import psql_queries
from database import vedis_queries
from algorythms import main
from handlers.text_handler import main_text_handler
import random
import datetime
from commands.for_orgs import status_change
from commands.for_orgs import Write_to_person
from commands.for_orgs import Regchange

#
# на случай, если бот не сможет подключиться к северу телеги из-за блокировки РКН
#
# apihelper.proxy={"https":"socks5://198.199.120.1002:1080"}

flag_reg_start = random.uniform(0, 20)

bot = config.get_bot()

connection = psql_queries.get_db_connection()

cursor = connection.cursor()

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
def reg_change_online(msg):
    Regchange.step_0(msg)


@bot.message_handler(commands=['change'])
def change_online_step_0(msg):
    if status_change.step_0(msg):
        bot.register_next_step_handler(msg, change_online_step_1)


def change_online_step_1(msg):
    if status_change.step_1(msg):
        bot.register_next_step_handler(msg, change_online_step_2)


def change_online_step_2(msg):
    status_change.step_2(msg)


@bot.message_handler(commands=['leave'])
def leave1(msg):
    global flag_reg_start
    if psql_queries.work_type(msg, 1):
        bot.send_message(msg.chat.id, 'Куда ты собрался выселяться. Ты орг')
    elif psql_queries.work_type(msg, 2):
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
            vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
            vedis_queries.set_var(msg.chat.id, 'mes_to_del2', mes1.message_id)
            if vedis_queries.get_var(msg.chat.id, 'mes_to_del3') != mes.message_id:
                try:
                    bot.delete_message(msg.chat.id, int(vedis_queries.get_var(msg.chat.id, 'mes_to_del3')))
                    bot.delete_message(msg.chat.id, int(vedis_queries.get_var(msg.chat.id, 'mes_to_del4')))
                except Exception:
                    pass
            vedis_queries.set_var(msg.chat.id, 'mes_to_del3', mes.message_id)
            vedis_queries.set_var(msg.chat.id, 'mes_to_del4', mes1.message_id)
            vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
            # если во время выселения что-то крашнулось, надо сбросить все переменные,
            # иначе какая-то из кнопок выселения не сработает
            vedis_queries.set_var(msg.chat.id, 'leave_yes', '0')
            vedis_queries.set_var(msg.chat.id, 'taken', '0')
            vedis_queries.set_var(msg.chat.id, 'key', '0')
            vedis_queries.set_var(msg.chat.id, 'no_key', '0')
            vedis_queries.set_var(msg.chat.id, 'accept', '0')


@bot.message_handler(commands=['info'])
def text(msg):
    if psql_queries.inform_state(msg) and psql_queries.work_type(msg, 1):
        bot.send_message(msg.chat.id, 'Введи текст, который будет отправлен всем участникам')
        bot.register_next_step_handler(msg, info)
    else:
        main.no_permis(msg)


def info(msg):
    cursor.execute(''' select chat_id from ev_people where status=2''')
    chat_id = cursor.fetchall()
    bot.send_message(msg.chat.id, 'Доставлено.')
    for i in chat_id:
        if msg.text != None:
            bot.send_message(i[0], msg.text)
        if msg.photo != None:
            photo = msg.photo[-1].file_id
            bot.send_photo(i[0], photo)


@bot.message_handler(commands=['add'])
def add(msg):
    if (psql_queries.inform_state(msg) and psql_queries.work_type(msg, 1)) or msg.chat.id == config.admin.Dav.value:
        bot.send_message(msg.chat.id, 'Введите номер человека, которого нужно добавить ')
        bot.register_next_step_handler(msg, add2)
    else:
        main.no_permis(msg)


def add2(msg):
    try:
        a = int(msg.text)
        cursor.execute(''' select p.p_id from ev_people p where p.p_id='%s' ''' % (a))
        rows = cursor.fetchall()
        if len(rows) > 0:

            cursor.execute('''insert into spec values('%s',0,TRUE)''' % (a))
            connection.commit()
            bot.send_message(msg.chat.id, 'Добавлено')
        else:
            bot.send_message(msg.chat.id, 'такого человека нет')
    except Exception:
        bot.send_message(msg.chat.id, 'ошибка в номере')


@bot.message_handler(commands=['surname'])
def add(msg):
    if psql_queries.work_type(msg, 1):
        bot.send_message(msg.chat.id, 'Введите фамилию человека, которого нужно найти ')
        bot.register_next_step_handler(msg, add3)
    else:
        main.no_permis(msg)


def add3(msg):
    try:
        a = str(msg.text)
        a.capitalize()
        cursor.execute(
            ''' select * from roomnum r where (select similarity(r.family_name,'%s'))>0.3 ''' % (
                a))
        rows = cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                bot.send_message(msg.chat.id,
                                 f' Личный номер: {row[0]}\n{row[3]} {row[2]} {row[1]} \nНомер телефона: {row[4]}\nГруппа {row[6]}\nНомер комнаты: {row[5]}')
        else:
            bot.send_message(msg.chat.id, 'такого человека нет')
    except Exception:
        bot.send_message(msg.chat.id, 'ошибка в фамимлии')


@bot.message_handler(commands=['roomnum'])
def add(msg):
    if psql_queries.work_type(msg, 1):
        bot.send_message(msg.chat.id, 'Введите номер комнаты ')
        bot.register_next_step_handler(msg, add22)
    else:
        main.no_permis(msg)


def add22(msg):
    try:
        a = int(msg.text)
        cursor.execute(
            ''' select * from roomnum r where r.room='%s' ''' % (
                a))
        rows = cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                bot.send_message(msg.chat.id,
                                 f' Личный номер: {row[0]}\n{row[3]} {row[2]} {row[1]} \nНомер телефона: {row[4]}\nГруппа {row[6]}\nНомер комнаты: {row[5]}')
        else:
            bot.send_message(msg.chat.id, 'такой комнаты нет')
    except Exception:
        bot.send_message(msg.chat.id, 'ошибка в номере')


@bot.message_handler(commands=['help'])
#
# функция команды /help
#
def help_message(msg):
    if psql_queries.work_type(msg, 1):
        bot.send_message(msg.chat.id,
                         config.Help_text.help_part.value)
    else:
        bot.send_message(msg.chat.id,
                         config.Help_text.help_org.value)


@bot.message_handler(commands=['write'])
#
# функция команды /write которая позволяет написать в личку человеку по его id
#
def white_online_step_0(msg):
    if Write_to_person.step_0(msg):
        bot.register_next_step_handler(msg, write_online_step_1)


def write_online_step_1(msg):
    Write_to_person.step_1(msg)
    bot.register_next_step_handler(msg, write_online_step_2)


def write_online_step_2(msg):
    Write_to_person.step_2(msg)


@bot.message_handler(commands=['lmoder'])
def peopleshow(msg):
    if psql_queries.work_type(msg, 1):
        cursor.execute("""select p.first_name,p.middle_name,s.inform from spec s,ev_people p where p.p_id=s.spec_id""")
        rows = cursor.fetchall()
        for r in rows:
            bot.send_message(msg.chat.id, (f"  {r[1]}  {r[0]}  наличие доступа: {r[2]}  "))
    else:
        main.no_permis(msg)


@bot.message_handler(commands=['listreg'])
def peopleshow(msg):
    if psql_queries.work_type(msg, 1):
        cursor.execute(
            """select count(p.p_id) from ev_people p,organizators org where org.regist=true and org.org_id=p.p_id """)
        rows = cursor.fetchall()
        bot.send_message(msg.chat.id, ' Количество выселяющих:%s' % (rows[0][0]))
        cursor.execute(
            """select p.first_name,p.middle_name from ev_people p,organizators org where org.regist=true and org.org_id=p.p_id""")
        rows = cursor.fetchall()
        for r in rows:
            bot.send_message(msg.chat.id, (f"  {r[1]}  {r[0]}   "))
    else:
        main.no_permis(msg)


@bot.message_handler(commands=['count'])
def peopleshow(msg):
    if psql_queries.work_type(msg, 1):
        cursor.execute("""select count(*) from ev_people """)
        rows = cursor.fetchall()
        for r in rows:
            bot.send_message(msg.chat.id, (f"  {r[0]}   "))
    else:
        main.no_permis(msg)


# вопрос юзеру по выбору роли
@bot.message_handler(commands=['start'])
# проверка по username и занесение в базу chat_id
# 0 - никто, 1 - орг, 2 - участник
def start_message(msg):
    if vedis_queries.get_state(msg.chat.id) == config.States.S_START.value or vedis_queries.get_state(
            msg.chat.id) == config.States.S_ENTER_RiGHT.value or vedis_queries.get_state(
        msg.chat.id) is None:

        if psql_queries.in_base(msg):
            if psql_queries.work_type(msg, 0):

                photo = open('images/Who.jpg', 'rb')
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
    bot.send_message(msg.chat.id, 'Изменение статуса произошло успешно.\nПереход в основное меню', reply_markup=Menu)

    if msg.text != 'Я булочка без начинки':
        if msg.text == 'Организатор':
            cursor.execute(
                ''' update ev_people set status='%s',p_id=nextval('seq_org')  where chat_id='%s'; insert into organizators select p.p_id from ev_people p where p.chat_id='%s' ''' % (
                    1, msg.chat.id, msg.chat.id))
            connection.commit()
        else:
            cursor.execute(
                ''' update ev_people set status='%s',p_id=nextval('seq_part') where chat_id='%s'; insert into participants select p.p_id from ev_people p where p.chat_id='%s' ''' % (
                    2, msg.chat.id, msg.chat.id))
            connection.commit()


@bot.message_handler(commands=['reg'])
def start_message1(msg):
    vedis_queries.set_none(msg.chat.id)
    if not psql_queries.in_base(msg):
        global flag_reg_start

        vedis_queries.set_var(msg.chat.id, 'flag_reg_start', flag_reg_start)

        vedis_queries.set_var(msg.chat.id, 'Username', msg.from_user.username)

        vedis_queries.set_var(msg.chat.id, 'Chatid', msg.chat.id)

        mes = bot.send_message(msg.chat.id,
                               'Попробуйте о себе что-нибудь вспомнить.\nНажимая "Хорошо", вы даете согласие на обработку персональных данных',
                               reply_markup=Keyok)

        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_NAME.value)

        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        bot.send_message(msg.chat.id, 'Ты уже в базе')


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_NAME.value and isinstance(msg.text,
                                                                                                             str))
def name(msg):
    global flag_reg_start

    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, text=config.Questions.Name.value)
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_MIDDLE.value)
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_MIDDLE.value and isinstance(msg.text,
                                                                                                               str))
def Family(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):

        vedis_queries.set_var(msg.chat.id, 'Name', msg.text)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Middle.value, reply_markup=Kname)
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_FAMILY.value)

        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_FAMILY.value and isinstance(msg.text,
                                                                                                               str))
def Middle(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):

        vedis_queries.set_var(msg.chat.id, 'Family', msg.text)

        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        mes = bot.send_message(msg.chat.id, text=config.Questions.Family.value, reply_markup=Kmiddle)

        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_GROUP.value)
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_GROUP.value and isinstance(msg.text,
                                                                                                              str))
def Group(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):

        vedis_queries.set_var(msg.chat.id, 'Middle', msg.text)

        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        mes = bot.send_message(msg.chat.id, text=config.Questions.Group.value, reply_markup=Kfamily)
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_PHONE.value)
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_PHONE.value and isinstance(msg.text,
                                                                                                              str))
def Phone(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        vedis_queries.set_var(msg.chat.id, 'Group', msg.text)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Phone.value, reply_markup=Kphone)

        vedis_queries.set_var(msg.chat.id, 'last_key_mes', mes.message_id)

        mes = bot.send_message(msg.chat.id, text=config.Questions.PhoneQ.value, reply_markup=Kgroup)

        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_DATE.value)

        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(content_types=[
    'contact'])
def Bdate(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start') and vedis_queries.get_state(
            msg.chat.id) == config.States.S_ENTER_DATE.value:
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'last_key_mes'))
        except Exception:
            pass

        if int(vedis_queries.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(vedis_queries.get_var(msg.chat.id, 'len')):
                try:
                    bot.delete_message(msg.chat.id, int(vedis_queries.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
            vedis_queries.set_var(msg.chat.id, 'len', 0)

        vedis_queries.set_var(msg.chat.id, 'Phone', msg.contact.phone_number)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Date.value)

        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_VKURL.value)

        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(content_types=['text'],
                     func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_DATE.value)
def wrong_phone(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, 'Нажми на кнопку в доп. клавиатуре')
        i = vedis_queries.get_var(msg.chat.id, 'len')
        vedis_queries.set_var(msg.chat.id, i, mes.message_id)
        vedis_queries.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        vedis_queries.set_var(msg.chat.id, 'len', str(int(i) + 2))

    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_VKURL.value and isinstance(msg.text,
                                                                                                              str) and vedis_queries.validate(
        msg.text))
def VKurl(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):
        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass

        vedis_queries.set_var(msg.chat.id, 'Date', msg.text)
        if int(vedis_queries.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(vedis_queries.get_var(msg.chat.id, 'len')):
                try:
                    bot.delete_message(msg.chat.id, int(vedis_queries.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
            vedis_queries.set_var(msg.chat.id, 'len', 0)

        mes = bot.send_message(msg.chat.id, text=config.Questions.Vk.value, reply_markup=Kdate)

        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_STOP.value)

        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                         reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_VKURL.value and isinstance(msg.text,
                                                                                                              str) and not vedis_queries.validate(
        msg.text))
def wrong_date(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, 'Неправильный формат даты')
        i = vedis_queries.get_var(msg.chat.id, 'len')
        vedis_queries.set_var(msg.chat.id, str(i), mes.message_id)

        vedis_queries.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        vedis_queries.set_var(msg.chat.id, 'len', str(int(i) + 2))
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: vedis_queries.get_state(msg.chat.id) == config.States.S_ENTER_STOP.value and isinstance(msg.text,
                                                                                                             str))
def last_message1(msg):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(msg.chat.id, 'flag_reg_start'):

        vedis_queries.set_var(msg.chat.id, 'VK', msg.text)
        if int(vedis_queries.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(vedis_queries.get_var(msg.chat.id, 'len')):
                try:
                    bot.delete_message(msg.chat.id, int(vedis_queries.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
            vedis_queries.set_var(msg.chat.id, 'len', 0)

        try:
            bot.delete_message(msg.chat.id, vedis_queries.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        question = 'Вас зовут ' + vedis_queries.get_var(msg.chat.id, 'Family') + ' ' + vedis_queries.get_var(
            msg.chat.id,
            'Name') + ' ' + vedis_queries.get_var(
            msg.chat.id, 'Middle') + '. Дата рождения' + vedis_queries.get_var(msg.chat.id,
                                                                               'Date') + '. Группа-' + vedis_queries.get_var(
            msg.chat.id, 'Group') + '. Номер телефона:' + vedis_queries.get_var(msg.chat.id,
                                                                                'Phone') + '. Ссылка на вк- ' + vedis_queries.get_var(
            msg.chat.id, 'VK') + '. Верно ?'
        mes = bot.send_message(msg.from_user.id, text=question, reply_markup=keyboardinlineYN)

        vedis_queries.set_var(msg.chat.id, 'user_wrong', msg.message_id)

        vedis_queries.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        vedis_queries.set_state(msg.chat.id, config.States.S_ENTER_RiGHT)
    else:
        vedis_queries.set_state(msg.chat.id, config.States.S_START.value)
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)


@bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    global flag_reg_start
    if str(flag_reg_start) == vedis_queries.get_var(call.message.chat.id, 'flag_reg_start'):
        if call.data == "yes" and vedis_queries.get_var(call.message.chat.id, 'flag_stop') != 'False':
            vedis_queries.set_var(call.message.chat.id, 'flag_stop', 'True')
            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
            except Exception:
                pass
            psql_queries.insert_new(call.message)
            bot.send_message(call.message.chat.id, text=config.Questions.Stop.value)
            vedis_queries.set_state(call.message.chat.id, config.States.S_ENTER_RiGHT.value)

            vedis_queries.set_none(call.message.chat.id)
        elif call.data == "no" and vedis_queries.get_var(call.message.chat.id, 'flag_stop') != 'True':
            vedis_queries.set_state(call.message.chat.id, config.States.S_START.value)
            vedis_queries.set_var(call.message.chat.id, 'flag_stop', 'False')
            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
            except Exception:
                pass
            bot.send_message(call.message.chat.id, 'Хм. Придется снова пройти этап регистрации', reply_markup=Keyreg)
        elif call.data == 'name' and vedis_queries.get_state(
                call.message.chat.id) != config.States.S_ENTER_MIDDLE.value:
            vedis_queries.set_state(call.message.chat.id, config.States.S_ENTER_MIDDLE.value)
            mes = bot.send_message(call.message.chat.id, 'Ну как ты так, вроде имя - одно.\n А как правильно ?')
            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'middle' and vedis_queries.get_state(
                call.message.chat.id) != config.States.S_ENTER_FAMILY.value:
            vedis_queries.set_state(call.message.chat.id, config.States.S_ENTER_FAMILY.value)
            mes = bot.send_message(call.message.chat.id, 'Ну как ты так, фамилию забыл.\n А как правильно ?')

            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'family' and vedis_queries.get_state(
                call.message.chat.id) != config.States.S_ENTER_GROUP.value:
            vedis_queries.set_state(call.message.chat.id, config.States.S_ENTER_GROUP.value)
            mes = bot.send_message(call.message.chat.id, 'Блен на тоби отец обидится.\n Какое у тебя отчество?')
            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'group' and vedis_queries.get_state(
                call.message.chat.id) != config.States.S_ENTER_PHONE.value:
            vedis_queries.set_state(call.message.chat.id, config.States.S_ENTER_PHONE.value)
            mes = bot.send_message(call.message.chat.id, 'Тебя будут хейтить одногруппники.\n Какая группа ?')
            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'user_wrong'))
                bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'last_key_mes'))
            except Exception:
                pass
            vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)

        elif call.data == 'date' and vedis_queries.get_state(call.message.chat.id) != config.States.S_ENTER_VKURL.value:
            vedis_queries.set_state(call.message.chat.id, config.States.S_ENTER_VKURL.value)
            mes = bot.send_message(call.message.chat.id,
                                   'Подсказка - в этот день ты родился.\n Напиши, если вспомнил(а)')
            try:
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(call.message.chat.id, vedis_queries.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
    elif vedis_queries.get_state(call.message.chat.id) != config.States.S_START.value and vedis_queries.get_state(
            call.message.chat.id) != config.States.S_ENTER_RiGHT.value:
        bot.send_message(call.message.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                         reply_markup=Keyreg)

    if call.data == 'leave_yes' and vedis_queries.get_var(call.message.chat.id, 'leave_yes') != '1':
        vedis_queries.set_var(call.message.chat.id, 'leave_yes', '1')
        mes = bot.send_message(call.message.chat.id,
                               'Заявка принята. В течение 1-5 минут к Вашей комнате подойдет организатор. Пожалуйста, не уходите далеко от своего номера.')
        if vedis_queries.get_var(call.message.chat.id, 'mes_to_del') != 0:
            try:
                bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del2'))
            except Exception:
                pass
        vedis_queries.set_var(call.message.chat.id, 'mes_to_del', 0)
        vedis_queries.set_var(call.message.chat.id, 'mes_to_del2', 0)

        cursor.execute(
            '''select p.p_id,p.family_name,p.first_name,p.middle_name from ev_people p where chat_id='%d' ''' % (
                call.message.chat.id))  # айди выселяющегося
        pid = cursor.fetchall()

        cursor.execute(''' insert into leave( participant_chat_id,time,participant_id) values('%s','%s','%s')''' % (
            call.message.chat.id, datetime.datetime.now().strftime("%H:%M:%S"), pid[0][0]))

        connection.commit()
        cursor.execute(
            ''' select p.chat_id from ev_people p,organizators org where org.regist=true and org.org_id=p.p_id''')  # те, кто может выселить
        rows = cursor.fetchall()

        accept = types.InlineKeyboardMarkup()
        accept_button = types.InlineKeyboardButton(text='Принять заявку',
                                                   callback_data='taken' + str(call.message.chat.id))
        accept.add(accept_button)
        for row in rows:
            mes = bot.send_message(row[0], '%s %s %s под номером %d хочет выселиться. ' % (
                pid[0][1], pid[0][2], pid[0][3], pid[0][0]),
                                   # Добавить потом комнату  первака
                                   reply_markup=accept)
            cursor.execute(
                ''' insert into msg_delivery( participant_chat_id, organizer_chat_id, msg_id, time) VALUES('%d','%d','%d','%s') ''' % (
                    call.message.chat.id, row[0], mes.message_id, datetime.datetime.now().strftime("%H:%M:%S")))
            connection.commit()

    elif call.data == 'leave_not' and vedis_queries.get_var(call.message.chat.id, 'leave_not') != '1':
        vedis_queries.set_var(call.message.chat.id, 'leave_not', '1')
        mes = bot.send_message(call.message.chat.id, 'Заявка отклонена.')
        if vedis_queries.get_var(call.message.chat.id, 'mes_to_del') != 0:
            try:
                bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
                bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del2'))
            except Exception:
                pass
        vedis_queries.set_var(call.message.chat.id, 'mes_to_del', 0)
        vedis_queries.set_var(call.message.chat.id, 'mes_to_del2', 0)
        vedis_queries.set_state(call.message.chat.id, config.States.S_START.value)
        vedis_queries.set_var(call.message.chat.id, 'leave_not', '0')

    elif 'taken' in call.data and vedis_queries.get_var(call.message.chat.id, 'taken') != '1':
        vedis_queries.set_var(call.message.chat.id, 'taken', '1')
        cursor.execute(
            ''' select m.organizer_chat_id,msg_id,l.participant_id from msg_delivery m,leave l where m.participant_chat_id=l.participant_chat_id and m.state=true and l.participant_chat_id='%s' ''' % (
                call.data[5:len(call.data):1]))
        rows = cursor.fetchall()
        for row in rows:
            try:
                bot.delete_message(row[0], row[1])
            except Exception:
                pass
        cursor.execute(''' update msg_delivery set state=False where participant_chat_id='%s' ''' % (rows[0][2]))
        connection.commit()
        mes = bot.send_message(call.message.chat.id, 'Выселить человека под номером %s ?' % (rows[0][2]),
                               reply_markup=accept_reject)
        vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        vedis_queries.set_var(call.message.chat.id, 'member', call.data[5:len(call.data):1])
        vedis_queries.set_var(call.message.chat.id, 'memberid', rows[0][2])
    elif call.data == 'accept' and vedis_queries.get_var(call.message.chat.id, 'accept') != '1':
        vedis_queries.set_var(call.message.chat.id, 'accept', '1')
        vedis_queries.set_state(int(vedis_queries.get_var(call.message.chat.id, 'member')), config.States.S_START.value)

        mes = bot.send_message(call.message.chat.id, ' Есть ли у него ключ от номера ?', reply_markup=key)

        try:
            bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        vedis_queries.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        cursor.execute(
            ''' update leave set state=True,check_out='%s' where participant_chat_id='%s' ''' % (
                datetime.datetime.now().strftime("%H:%M:%S"), vedis_queries.get_var(call.message.chat.id, 'member')))
        connection.commit()
    elif call.data == 'reject' and vedis_queries.get_var(call.message.chat.id, 'reject') != '1':
        vedis_queries.set_var(call.message.chat.id, 'reject', '1')
        vedis_queries.set_var(call.message.chat.id, 'taken', '0')
        vedis_queries.set_var(call.message.chat.id, 'accept', '0')
        vedis_queries.set_var(vedis_queries.get_var(call.message.chat.id, 'member'), 'leave_yes', '0')

        vedis_queries.set_state((call.message.chat.id, 'member'), config.States.S_START.value)
        bot.send_message(int(vedis_queries.get_var(call.message.chat.id, 'member')),
                         'Отказано в выселении.')
        mes = bot.send_message(call.message.chat.id,
                               '%s-му отказано в выселении.' % (
                                   vedis_queries.get_var(call.message.chat.id, 'memberid')))
        try:
            bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        cursor.execute(
            ''' delete from leave where participant_chat_id='%s'; delete from msg_delivery where participant_chat_id='%s'; ''' % (
                vedis_queries.get_var(call.message.chat.id, 'member'),
                vedis_queries.get_var(call.message.chat.id, 'member')))

        connection.commit()
        vedis_queries.set_var(call.message.chat.id, 'reject', '0')

    elif call.data == 'key' and vedis_queries.get_var(call.message.chat.id, 'key') != '1':
        vedis_queries.set_var(call.message.chat.id, 'key', '1')
        vedis_queries.set_var(call.message.chat.id, 'taken', '0')
        vedis_queries.set_var(call.message.chat.id, 'accept', '0')
        vedis_queries.set_var(vedis_queries.get_var(call.message.chat.id, 'member'), 'leave_yes', '0')

        mes = bot.send_message(call.message.chat.id,
                               '%s-мой выселен.' % (vedis_queries.get_var(call.message.chat.id, 'memberid')))
        try:
            bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        cursor.execute(
            ''' update leave set key=True where participant_chat_id='%s'; update msg_delivery set state=False where participant_chat_id='%s' ''' % (
                vedis_queries.get_var(call.message.chat.id, 'member'),
                vedis_queries.get_var(call.message.chat.id, 'member')))
        connection.commit()
        bot.send_message(vedis_queries.get_var(call.message.chat.id, 'member'),
                         'Подойдите к стойке регистрации. Вас будут там ожидать.')
        vedis_queries.set_var(call.message.chat.id, 'key', '0')

    elif call.data == 'no_key' and vedis_queries.get_var(call.message.chat.id, 'no_key') != '1':
        vedis_queries.set_var(call.message.chat.id, 'no_key', '1')
        vedis_queries.set_var(call.message.chat.id, 'taken', '0')
        vedis_queries.set_var(call.message.chat.id, 'accept', '0')
        vedis_queries.set_var(call.message.chat.id, 'leave_yes', '0')

        mes = bot.send_message(call.message.chat.id,
                               'чеовек с номером %s выселен.' % (
                                   vedis_queries.get_var(call.message.chat.id, 'memberid')))
        bot.send_message(vedis_queries.get_var(call.message.chat.id, 'member'),
                         'Подойдите к стойке регистрации. Вас будут там ожидать.')
        try:
            bot.delete_message(mes.chat.id, vedis_queries.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        cursor.execute(
            ''' update leave set state=False where participant_chat_id='%s' ''' % (
                vedis_queries.get_var(call.message.chat.id, 'member')))

        connection.commit()
        vedis_queries.set_var(call.message.chat.id, 'no_key', '0')


@bot.message_handler(content_types=['text'])
def send_text(msg):
    main_text_handler(msg)


#
# прослушивание сервера телеги на наличие новых сообщений
#
bot.polling()
