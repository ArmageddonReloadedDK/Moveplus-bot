from telebot import types
from settings import config
from algorythms import main
from base.human import Human_class
from handlers.text_handler import main_text_handler
import random
import datetime

from org_commands.reg_change import Regchange

#
# на случай, если бот не сможет подключиться к северу телеги из-за блокировки РКН
#
# apihelper.proxy={"https":"socks5://198.199.120.1002:1080"}

flag_reg_start = random.uniform(0, 20)

human = Human_class()
cursor = human.cursor
bot = human.bot

KeyYN = types.ReplyKeyboardMarkup(True, True)
KeyYN.row('Да', 'Нет')

Keybivaet = types.ReplyKeyboardMarkup(True, True)
Keybivaet.row('Напишу правильно в следующем сообщении')

Keyreg = types.ReplyKeyboardMarkup(True, True)
Keyreg.row('/reg')

Keyok = types.ReplyKeyboardMarkup(True, True)
Keyok.row('Хорошо')

keyboard2 = types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Я не Саня', 'Я сладкий пирожочек')

keyboard3 = types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Участник', 'Организатор', 'Я булочка без начинки')

MenuPosv = types.ReplyKeyboardMarkup(True, True)
MenuPosv.row('Жилье', 'Карта', 'Ночные точки', 'Нужна мед помощь', 'Дестрой')

Key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
Key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboardinlineYN = types.InlineKeyboardMarkup()
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


#########################################
#
# отредачил функции
#
@bot.message_handler(commands=['regchange'])
def reg_change_online(msg):
    human.reg_status.registraion_change_step_0(msg)


@bot.message_handler(commands=['change'])
def change_online_step_0(msg):
    if human.status.status_change_step_0(msg):
        human.bot.register_next_step_handler(msg, change_online_step_1)


def change_online_step_1(msg):
    if human.status.status_change_step_1(msg):
        human.bot.register_next_step_handler(msg, change_online_step_2)


def change_online_step_2(msg):
    human.status.status_change_step_2(msg)


@bot.message_handler(commands=['help'])
#
# функция команды /help
#
def help_message(msg):
    if human.work_type(msg, 1):
        human.bot.send_message(msg.chat.id,
                               config.Help_text.help_part.value)
    else:
        human.bot.send_message(msg.chat.id,
                               config.Help_text.help_org.value)


@bot.message_handler(commands=['write'])
#
# функция команды /write которая позволяет написать в личку человеку по его id
#
def white_online_step_0(msg):
    if human.write_to_person.write_to_person_step_0(msg):
        human.bot.register_next_step_handler(msg, write_online_step_1)


def write_online_step_1(msg):
    human.write_to_person.write_to_person_step_1(msg)
    human.bot.register_next_step_handler(msg, write_online_step_2)


def write_online_step_2(msg):
    human.write_to_person.write_to_person_step_2(msg)


@bot.message_handler(commands=['family'])
#
# нечеткий поиск человека по фамилии
#
def family_search_online_step_0(msg):
    if human.family_search.family_search_step_0(msg):
        human.bot.register_next_step_handler(msg, family_search_online_step_1)


def family_search_online_step_1(msg):
    human.family_search.family_search_step_1(msg)

###################################################################

@bot.message_handler(commands=['leave'])
def leave1(msg):
    global flag_reg_start
    if human.work_type(msg, 1):
        human.bot.send_message(msg.chat.id, 'Куда ты собрался выселяться. Ты орг')
    elif human.work_type(msg, 2):
        cursor.execute(''' select l.state  from leave l  where l.participant_chat_id='%s' ''' % (msg.chat.id))
        rows = cursor.fetchall()
        if len(rows) > 0:
            if not rows[0][0]:
                human.bot.send_message(msg.chat.id, 'Заявка уже отправлена. Пожалуйста, ожидайте')
            elif rows[0][0]:
                human.bot.send_message(msg.chat.id, 'Вы уже покинули мероприятие :)')
        else:
            mes = human.bot.send_message(msg.chat.id, 'Насколько я понимаю, Вы хотите покинуть мероприятие.')
            mes1 = human.bot.send_message(msg.chat.id, ' Подтверждаете заявку?', reply_markup=leave_yes_not)
            human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
            human.set_var(msg.chat.id, 'mes_to_del2', mes1.message_id)
            if human.get_var(msg.chat.id, 'mes_to_del3') != mes.message_id:
                try:
                    human.bot.delete_message(msg.chat.id, int(human.get_var(msg.chat.id, 'mes_to_del3')))
                    human.bot.delete_message(msg.chat.id, int(human.get_var(msg.chat.id, 'mes_to_del4')))
                except Exception:
                    pass
            human.set_var(msg.chat.id, 'mes_to_del3', mes.message_id)
            human.set_var(msg.chat.id, 'mes_to_del4', mes1.message_id)
            human.set_state(msg.chat.id, config.States.S_START.value)
            # если во время выселения что-то крашнулось, надо сбросить все переменные,
            # иначе какая-то из кнопок выселения не сработает
            human.set_var(msg.chat.id, 'leave_yes', '0')
            human.set_var(msg.chat.id, 'taken', '0')
            human.set_var(msg.chat.id, 'key', '0')
            human.set_var(msg.chat.id, 'no_key', '0')
            human.set_var(msg.chat.id, 'accept', '0')


@bot.message_handler(commands=['write_ev'])
def text(msg):
    if human.inform_state(msg) and human.work_type(msg, 1):
        human.bot.send_message(msg.chat.id, 'Введи текст, который будет отправлен всем участникам')
        human.bot.register_next_step_handler(msg, info)
    else:
        main.no_permis(msg)


def info(msg):
    cursor.execute(''' select chat_id from ev_people where status=2''')
    chat_id = cursor.fetchall()
    human.bot.send_message(msg.chat.id, 'Доставлено.')
    for i in chat_id:
        if msg.text != None:
            human.bot.send_message(i[0], msg.text)
        if msg.photo != None:
            photo = msg.photo[-1].file_id
            human.bot.send_photo(i[0], photo)


@bot.message_handler(commands=['add_mod'])
#
#  добавление орга в список модераторов
#
def add(msg):
    if (human.inform_state(msg) and human.work_type(msg, 1)) or msg.chat.id == config.admin.Dav.value:
        human.bot.send_message(msg.chat.id, 'Введите номер человека, которого нужно добавить ')
        human.bot.register_next_step_handler(msg, add2)
    else:
        main.no_permis(msg)


def add2(msg):
    try:
        a = int(msg.text)
        cursor.execute(''' select p.p_id from ev_people p where p.p_id='%s' ''' % (a))
        rows = cursor.fetchall()
        if len(rows) > 0:

            cursor.execute('''insert into spec values('%s',0,TRUE)''' % (a))
            human.connection.commit()
            human.bot.send_message(msg.chat.id, 'Добавлено')
        else:
            human.bot.send_message(msg.chat.id, 'такого человека нет')
    except Exception:
        human.bot.send_message(msg.chat.id, 'ошибка в номере')


@bot.message_handler(commands=['roomnum'])
def add(msg):
    if human.work_type(msg, 1):
        human.bot.send_message(msg.chat.id, 'Введите номер комнаты ')
        human.bot.register_next_step_handler(msg, add22)
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
                human.bot.send_message(msg.chat.id,
                                       f' Личный номер: {row[0]}\n{row[3]} {row[2]} {row[1]} \nНомер телефона: {row[4]}\nГруппа {row[6]}\nНомер комнаты: {row[5]}')
        else:
            human.bot.send_message(msg.chat.id, 'такой комнаты нет')
    except Exception:
        human.bot.send_message(msg.chat.id, 'ошибка в номере')


@bot.message_handler(commands=['lmoder'])
def peopleshow(msg):
    if human.work_type(msg, 1):
        cursor.execute("""select p.first_name,p.middle_name,s.inform from spec s,ev_people p where p.p_id=s.spec_id""")
        rows = cursor.fetchall()
        for r in rows:
            human.bot.send_message(msg.chat.id, (f"  {r[1]}  {r[0]}  наличие доступа: {r[2]}  "))
    else:
        main.no_permis(msg)


@bot.message_handler(commands=['listreg'])
def peopleshow(msg):
    if human.work_type(msg, 1):
        cursor.execute(
            """select count(p.p_id) from ev_people p,organizators org where org.regist=true and org.org_id=p.p_id """)
        rows = cursor.fetchall()
        human.bot.send_message(msg.chat.id, ' Количество выселяющих:%s' % (rows[0][0]))
        cursor.execute(
            """select p.first_name,p.middle_name from ev_people p,organizators org where org.regist=true and org.org_id=p.p_id""")
        rows = cursor.fetchall()
        for r in rows:
            human.bot.send_message(msg.chat.id, (f"  {r[1]}  {r[0]}   "))
    else:
        main.no_permis(msg)


@bot.message_handler(commands=['count'])
def peopleshow(msg):
    if human.work_type(msg, 1):
        cursor.execute("""select count(*) from ev_people """)
        rows = cursor.fetchall()
        for r in rows:
            human.bot.send_message(msg.chat.id, (f"  {r[0]}   "))
    else:
        main.no_permis(msg)


# вопрос юзеру по выбору роли
@bot.message_handler(commands=['start'])
# проверка по username и занесение в базу chat_id
# 0 - никто, 1 - орг, 2 - участник
def start_message(msg):
    if human.get_state(msg.chat.id) == config.States.S_START.value or human.get_state(
            msg.chat.id) == config.States.S_ENTER_RiGHT.value or human.get_state(
        msg.chat.id) is None:

        if human.in_base(msg):
            if human.work_type(msg, 0):

                photo = open('images/Who.jpg', 'rb')
                human.bot.send_photo(msg.chat.id, photo)

                human.bot.send_message(msg.chat.id,
                                       'Какая у тебя роль в событии ?\nВнимание! Этот пункт выбирается только один раз.\n',
                                       reply_markup=keyboard3)
                human.bot.register_next_step_handler(msg, login)

            else:
                human.bot.send_message(msg.chat.id,
                                       'Я же предупреждал. Уже не поменяешь :) \nНо если очень нужно, то пиши @ArmageddonReloaded',
                                       reply_markup=Menu)
        else:
            human.bot.send_message(msg.chat.id, 'Тебя еще нет в базе,\nвведи /reg.')


def login(msg):
    human.bot.send_message(msg.chat.id, 'Изменение статуса произошло успешно.\nПереход в основное меню',
                           reply_markup=Menu)

    if msg.text != 'Я булочка без начинки':
        if msg.text == 'Организатор':
            cursor.execute(
                ''' update ev_people set status='%s',p_id=nextval('seq_org')  where chat_id='%s'; insert into organizators select p.p_id from ev_people p where p.chat_id='%s' ''' % (
                    1, msg.chat.id, msg.chat.id))
            human.connection.commit()
        else:
            cursor.execute(
                ''' update ev_people set status='%s',p_id=nextval('seq_part') where chat_id='%s'; insert into participants select p.p_id from ev_people p where p.chat_id='%s' ''' % (
                    2, msg.chat.id, msg.chat.id))
            human.connection.commit()


@bot.message_handler(commands=['reg'])
def start_message1(msg):
    human.set_none(msg.chat.id)
    if not human.in_base(msg):
        global flag_reg_start

        human.set_var(msg.chat.id, 'flag_reg_start', flag_reg_start)

        human.set_var(msg.chat.id, 'Username', msg.from_user.username)

        human.set_var(msg.chat.id, 'Chatid', msg.chat.id)

        mes = human.bot.send_message(msg.chat.id,
                                     'Попробуйте о себе что-нибудь вспомнить.\nНажимая "Хорошо", вы даете согласие на обработку персональных данных',
                                     reply_markup=Keyok)

        human.set_state(msg.chat.id, config.States.S_ENTER_NAME.value)

        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.bot.send_message(msg.chat.id, 'Ты уже в базе')


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_NAME.value and isinstance(msg.text,
                                                                                                     str))
def name(msg):
    global flag_reg_start

    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):
        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Name.value)
        human.set_state(msg.chat.id, config.States.S_ENTER_MIDDLE.value)
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_MIDDLE.value and isinstance(msg.text,
                                                                                                       str))
def Family(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):

        human.set_var(msg.chat.id, 'Name', msg.text)

        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Middle.value, reply_markup=Kname)
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        human.set_state(msg.chat.id, config.States.S_ENTER_FAMILY.value)

        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_FAMILY.value and isinstance(msg.text,
                                                                                                       str))
def Middle(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):

        human.set_var(msg.chat.id, 'Family', msg.text)

        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Family.value, reply_markup=Kmiddle)

        human.set_state(msg.chat.id, config.States.S_ENTER_GROUP.value)
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_GROUP.value and isinstance(msg.text,
                                                                                                      str))
def Group(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):

        human.set_var(msg.chat.id, 'Middle', msg.text)

        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Group.value, reply_markup=Kfamily)
        human.set_state(msg.chat.id, config.States.S_ENTER_PHONE.value)
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_PHONE.value and isinstance(msg.text,
                                                                                                      str))
def Phone(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        human.set_var(msg.chat.id, 'Group', msg.text)

        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Phone.value, reply_markup=Kphone)

        human.set_var(msg.chat.id, 'last_key_mes', mes.message_id)

        mes = human.bot.send_message(msg.chat.id, text=config.Questions.PhoneQ.value, reply_markup=Kgroup)

        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        human.set_state(msg.chat.id, config.States.S_ENTER_DATE.value)

        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(content_types=[
    'contact'])
def Bdate(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start') and human.get_state(
            msg.chat.id) == config.States.S_ENTER_DATE.value:
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'last_key_mes'))
        except Exception:
            pass

        if int(human.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(human.get_var(msg.chat.id, 'len')):
                try:
                    human.bot.delete_message(msg.chat.id, int(human.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
            human.set_var(msg.chat.id, 'len', 0)

        human.set_var(msg.chat.id, 'Phone', msg.contact.phone_number)

        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Date.value)

        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        human.set_state(msg.chat.id, config.States.S_ENTER_VKURL.value)

        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(content_types=['text'],
                     func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_DATE.value)
def wrong_phone(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):
        mes = human.bot.send_message(msg.chat.id, 'Нажми на кнопку в доп. клавиатуре')
        i = human.get_var(msg.chat.id, 'len')
        human.set_var(msg.chat.id, i, mes.message_id)
        human.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        human.set_var(msg.chat.id, 'len', str(int(i) + 2))

    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_VKURL.value and isinstance(msg.text,
                                                                                                      str) and human.validate(
        msg.text))
def VKurl(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):
        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass

        human.set_var(msg.chat.id, 'Date', msg.text)
        if int(human.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(human.get_var(msg.chat.id, 'len')):
                try:
                    human.bot.delete_message(msg.chat.id, int(human.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
            human.set_var(msg.chat.id, 'len', 0)

        mes = human.bot.send_message(msg.chat.id, text=config.Questions.Vk.value, reply_markup=Kdate)

        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)
        human.set_state(msg.chat.id, config.States.S_ENTER_STOP.value)

        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_VKURL.value and isinstance(msg.text,
                                                                                                      str) and not human.validate(
        msg.text))
def wrong_date(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):
        mes = human.bot.send_message(msg.chat.id, 'Неправильный формат даты')
        i = human.get_var(msg.chat.id, 'len')
        human.set_var(msg.chat.id, str(i), mes.message_id)

        human.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        human.set_var(msg.chat.id, 'len', str(int(i) + 2))
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@bot.message_handler(
    func=lambda msg: human.get_state(msg.chat.id) == config.States.S_ENTER_STOP.value and isinstance(msg.text,
                                                                                                     str))
def last_message1(msg):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(msg.chat.id, 'flag_reg_start'):

        human.set_var(msg.chat.id, 'VK', msg.text)
        if int(human.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(human.get_var(msg.chat.id, 'len')):
                try:
                    human.bot.delete_message(msg.chat.id, int(human.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
            human.set_var(msg.chat.id, 'len', 0)

        try:
            human.bot.delete_message(msg.chat.id, human.get_var(msg.chat.id, 'mes_to_del'))
        except Exception:
            pass
        question = 'Вас зовут ' + human.get_var(msg.chat.id, 'Family') + ' ' + human.get_var(
            msg.chat.id,
            'Name') + ' ' + human.get_var(
            msg.chat.id, 'Middle') + '. Дата рождения' + human.get_var(msg.chat.id,
                                                                       'Date') + '. Группа-' + human.get_var(
            msg.chat.id, 'Group') + '. Номер телефона:' + human.get_var(msg.chat.id,
                                                                        'Phone') + '. Ссылка на вк- ' + human.get_var(
            msg.chat.id, 'VK') + '. Верно ?'
        mes = human.bot.send_message(msg.from_user.id, text=question, reply_markup=keyboardinlineYN)

        human.set_var(msg.chat.id, 'user_wrong', msg.message_id)

        human.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        human.set_state(msg.chat.id, config.States.S_ENTER_RiGHT)
    else:
        human.set_state(msg.chat.id, config.States.S_START.value)
        human.bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)


@human.bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    global flag_reg_start
    if str(flag_reg_start) == human.get_var(call.message.chat.id, 'flag_reg_start'):
        if call.data == "yes" and human.get_var(call.message.chat.id, 'flag_stop') != 'False':
            human.set_var(call.message.chat.id, 'flag_stop', 'True')
            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
            except Exception:
                pass
            human.insert_new(call.message)
            human.bot.send_message(call.message.chat.id, text=config.Questions.Stop.value)
            human.set_state(call.message.chat.id, config.States.S_ENTER_RiGHT.value)

            human.set_none(call.message.chat.id)
        elif call.data == "no" and human.get_var(call.message.chat.id, 'flag_stop') != 'True':
            human.set_state(call.message.chat.id, config.States.S_START.value)
            human.set_var(call.message.chat.id, 'flag_stop', 'False')
            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
            except Exception:
                pass
            human.bot.send_message(call.message.chat.id, 'Хм. Придется снова пройти этап регистрации',
                                   reply_markup=Keyreg)
        elif call.data == 'name' and human.get_state(
                call.message.chat.id) != config.States.S_ENTER_MIDDLE.value:
            human.set_state(call.message.chat.id, config.States.S_ENTER_MIDDLE.value)
            mes = human.bot.send_message(call.message.chat.id, 'Ну как ты так, вроде имя - одно.\n А как правильно ?')
            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'middle' and human.get_state(
                call.message.chat.id) != config.States.S_ENTER_FAMILY.value:
            human.set_state(call.message.chat.id, config.States.S_ENTER_FAMILY.value)
            mes = human.bot.send_message(call.message.chat.id, 'Ну как ты так, фамилию забыл.\n А как правильно ?')

            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'family' and human.get_state(
                call.message.chat.id) != config.States.S_ENTER_GROUP.value:
            human.set_state(call.message.chat.id, config.States.S_ENTER_GROUP.value)
            mes = human.bot.send_message(call.message.chat.id, 'Блен на тоби отец обидится.\n Какое у тебя отчество?')
            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        elif call.data == 'group' and human.get_state(
                call.message.chat.id) != config.States.S_ENTER_PHONE.value:
            human.set_state(call.message.chat.id, config.States.S_ENTER_PHONE.value)
            mes = human.bot.send_message(call.message.chat.id, 'Тебя будут хейтить одногруппники.\n Какая группа ?')
            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'user_wrong'))
                human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'last_key_mes'))
            except Exception:
                pass
            human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)

        elif call.data == 'date' and human.get_state(call.message.chat.id) != config.States.S_ENTER_VKURL.value:
            human.set_state(call.message.chat.id, config.States.S_ENTER_VKURL.value)
            mes = human.bot.send_message(call.message.chat.id,
                                         'Подсказка - в этот день ты родился.\n Напиши, если вспомнил(а)')
            try:
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(call.message.chat.id, human.get_var(call.message.chat.id, 'user_wrong'))
            except Exception:
                pass
            human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
    elif human.get_state(call.message.chat.id) != config.States.S_START.value and human.get_state(
            call.message.chat.id) != config.States.S_ENTER_RiGHT.value:
        human.bot.send_message(call.message.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново',
                               reply_markup=Keyreg)

    if call.data == 'leave_yes' and human.get_var(call.message.chat.id, 'leave_yes') != '1':
        human.set_var(call.message.chat.id, 'leave_yes', '1')
        mes = human.bot.send_message(call.message.chat.id,
                                     'Заявка принята. В течение 1-5 минут к Вашей комнате подойдет организатор. Пожалуйста, не уходите далеко от своего номера.')
        if human.get_var(call.message.chat.id, 'mes_to_del') != 0:
            try:
                human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del2'))
            except Exception:
                pass
        human.set_var(call.message.chat.id, 'mes_to_del', 0)
        human.set_var(call.message.chat.id, 'mes_to_del2', 0)

        cursor.execute(
            '''select p.p_id,p.family_name,p.first_name,p.middle_name from ev_people p where chat_id='%d' ''' % (
                call.message.chat.id))  # айди выселяющегося
        pid = cursor.fetchall()

        cursor.execute(''' insert into leave( participant_chat_id,time,participant_id) values('%s','%s','%s')''' % (
            call.message.chat.id, datetime.datetime.now().strftime("%H:%M:%S"), pid[0][0]))

        human.connection.commit()
        cursor.execute(
            ''' select p.chat_id from ev_people p,organizators org where org.regist=true and org.org_id=p.p_id''')  # те, кто может выселить
        rows = cursor.fetchall()

        accept = types.InlineKeyboardMarkup()
        accept_button = types.InlineKeyboardButton(text='Принять заявку',
                                                   callback_data='taken' + str(call.message.chat.id))
        accept.add(accept_button)
        for row in rows:
            mes = human.bot.send_message(row[0], '%s %s %s под номером %d хочет выселиться. ' % (
                pid[0][1], pid[0][2], pid[0][3], pid[0][0]),
                                         # Добавить потом комнату  первака
                                         reply_markup=accept)
            cursor.execute(
                ''' insert into msg_delivery( participant_chat_id, organizer_chat_id, msg_id, time) VALUES('%d','%d','%d','%s') ''' % (
                    call.message.chat.id, row[0], mes.message_id, datetime.datetime.now().strftime("%H:%M:%S")))
            human.connection.commit()

    elif call.data == 'leave_not' and human.get_var(call.message.chat.id, 'leave_not') != '1':
        human.set_var(call.message.chat.id, 'leave_not', '1')
        mes = human.bot.send_message(call.message.chat.id, 'Заявка отклонена.')
        if human.get_var(call.message.chat.id, 'mes_to_del') != 0:
            try:
                human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
                human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del2'))
            except Exception:
                pass
        human.set_var(call.message.chat.id, 'mes_to_del', 0)
        human.set_var(call.message.chat.id, 'mes_to_del2', 0)
        human.set_state(call.message.chat.id, config.States.S_START.value)
        human.set_var(call.message.chat.id, 'leave_not', '0')

    elif 'taken' in call.data and human.get_var(call.message.chat.id, 'taken') != '1':
        human.set_var(call.message.chat.id, 'taken', '1')
        cursor.execute(
            ''' select m.organizer_chat_id,msg_id,l.participant_id from msg_delivery m,leave l where m.participant_chat_id=l.participant_chat_id and m.state=true and l.participant_chat_id='%s' ''' % (
                call.data[5:len(call.data):1]))
        rows = cursor.fetchall()
        for row in rows:
            try:
                human.bot.delete_message(row[0], row[1])
            except Exception:
                pass
        cursor.execute(''' update msg_delivery set state=False where participant_chat_id='%s' ''' % (rows[0][2]))
        human.connection.commit()
        mes = human.bot.send_message(call.message.chat.id, 'Выселить человека под номером %s ?' % (rows[0][2]),
                                     reply_markup=accept_reject)
        human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        human.set_var(call.message.chat.id, 'member', call.data[5:len(call.data):1])
        human.set_var(call.message.chat.id, 'memberid', rows[0][2])
    elif call.data == 'accept' and human.get_var(call.message.chat.id, 'accept') != '1':
        human.set_var(call.message.chat.id, 'accept', '1')
        human.set_state(int(human.get_var(call.message.chat.id, 'member')), config.States.S_START.value)

        mes = human.bot.send_message(call.message.chat.id, ' Есть ли у него ключ от номера ?', reply_markup=key)

        try:
            human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        human.set_var(call.message.chat.id, 'mes_to_del', mes.message_id)
        cursor.execute(
            ''' update leave set state=True,check_out='%s' where participant_chat_id='%s' ''' % (
                datetime.datetime.now().strftime("%H:%M:%S"), human.get_var(call.message.chat.id, 'member')))
        human.connection.commit()
    elif call.data == 'reject' and human.get_var(call.message.chat.id, 'reject') != '1':
        human.set_var(call.message.chat.id, 'reject', '1')
        human.set_var(call.message.chat.id, 'taken', '0')
        human.set_var(call.message.chat.id, 'accept', '0')
        human.set_var(human.get_var(call.message.chat.id, 'member'), 'leave_yes', '0')

        human.set_state((call.message.chat.id, 'member'), config.States.S_START.value)
        human.bot.send_message(int(human.get_var(call.message.chat.id, 'member')),
                               'Отказано в выселении.')
        mes = human.bot.send_message(call.message.chat.id,
                                     '%s-му отказано в выселении.' % (
                                         human.get_var(call.message.chat.id, 'memberid')))
        try:
            human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        cursor.execute(
            ''' delete from leave where participant_chat_id='%s'; delete from msg_delivery where participant_chat_id='%s'; ''' % (
                human.get_var(call.message.chat.id, 'member'),
                human.get_var(call.message.chat.id, 'member')))

        human.connection.commit()
        human.set_var(call.message.chat.id, 'reject', '0')

    elif call.data == 'key' and human.get_var(call.message.chat.id, 'key') != '1':
        human.set_var(call.message.chat.id, 'key', '1')
        human.set_var(call.message.chat.id, 'taken', '0')
        human.set_var(call.message.chat.id, 'accept', '0')
        human.set_var(human.get_var(call.message.chat.id, 'member'), 'leave_yes', '0')

        mes = human.bot.send_message(call.message.chat.id,
                                     '%s-мой выселен.' % (human.get_var(call.message.chat.id, 'memberid')))
        try:
            human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        cursor.execute(
            ''' update leave set key=True where participant_chat_id='%s'; update msg_delivery set state=False where participant_chat_id='%s' ''' % (
                human.get_var(call.message.chat.id, 'member'),
                human.get_var(call.message.chat.id, 'member')))
        human.connection.commit()
        human.bot.send_message(human.get_var(call.message.chat.id, 'member'),
                               'Подойдите к стойке регистрации. Вас будут там ожидать.')
        human.set_var(call.message.chat.id, 'key', '0')

    elif call.data == 'no_key' and human.get_var(call.message.chat.id, 'no_key') != '1':
        human.set_var(call.message.chat.id, 'no_key', '1')
        human.set_var(call.message.chat.id, 'taken', '0')
        human.set_var(call.message.chat.id, 'accept', '0')
        human.set_var(call.message.chat.id, 'leave_yes', '0')

        mes = human.bot.send_message(call.message.chat.id,
                                     'чеовек с номером %s выселен.' % (
                                         human.get_var(call.message.chat.id, 'memberid')))
        human.bot.send_message(human.get_var(call.message.chat.id, 'member'),
                               'Подойдите к стойке регистрации. Вас будут там ожидать.')
        try:
            human.bot.delete_message(mes.chat.id, human.get_var(call.message.chat.id, 'mes_to_del'))
        except Exception:
            pass
        cursor.execute(
            ''' update leave set state=False where participant_chat_id='%s' ''' % (
                human.get_var(call.message.chat.id, 'member')))

        human.connection.commit()
        human.set_var(call.message.chat.id, 'no_key', '0')


@bot.message_handler(content_types=['text'])
def send_text(msg):
    main_text_handler(msg)


#
# прослушивание сервера телеги на наличие новых сообщений
#
human.bot.polling()
