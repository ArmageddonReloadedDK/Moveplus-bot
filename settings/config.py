from enum import Enum
import telebot

token = '616126274:AAGlRipQWcuwhgHdd83ThFvKchNfrf9ybqA'
db_file = "database/database.vdb"
db_vars = "database/varbase.vdb"


def get_bot():
    return telebot.TeleBot(token)


class States(Enum):
    S_PREP = "0"
    S_START = "1"
    S_ENTER_NAME = "2"
    S_ENTER_MIDDLE = "3"
    S_ENTER_FAMILY = "4"
    S_ENTER_GROUP = "5"
    S_ENTER_PHONE = "6"
    S_ENTER_DATE = "7"
    S_ENTER_VKURL = "8"
    S_ENTER_STOP = '9'
    S_ENTER_RiGHT = '10'
    S_busy = '11'
    S_busy_org = '13'
    S_not_busy = '12'


class Help_text(Enum):
    help_part = 'Бот в процессе разработки.Доступные команды: \n' \
                '/lmoder - список модераторов\n' \
                '/add - добавить модератора\n ' \
                '/change - изменить статус модератора\n' \
                '/listreg - список выселяющих организаторов\n' \
                '/surname - поиск людей по фамилии\n' \
                '/info - написать сообщение всем участникам\n' \
                '/write - написать конкретному человеку\n' \
                '/count - количество людей в базе\n' \
                '/roomnum - список жильцов одного номера \n' \
                '/regchange - готов/не готов выселять людей \n' \
                'Заметил косяк ? Пиши сюда @ArmageddonReloaded'

    help_org = 'Бот в процессе разработки.Доступные команды: \n' \
               '/start - начать процесс регистрации на мероприятии\n' \
               '/leave - подать заявку на выселение\n' \
               'Заметил косяк ? Пиши сюда @ArmageddonReloaded'


class Questions(Enum):
    Name = 'Как тебя зовут ?'
    Middle = 'Какая у тебя фамилия?'
    Family = 'А отчество (при наличии)?'
    Phone = 'Дальше нужен номер телефона\n(Нажми на кнопку в доп меню)'
    PhoneQ = '(чтобы мы смогли с тобой связаться)'
    Group = 'Теперь подскажи группу, в которой ты учишься.\n (Осталось совсем немного)'
    Date = 'Дальше - дата рождения в формате xx.xx.xxxx'
    Vk = 'И последнее. Скинь ссылку на твой вк'
    Stop = 'От души. Надеюсь, ты не ошибся(-лась) нигде. Но если ошибся(-лась) -\n' \
           ' тебе сюда @ArmageddonReloaded.' \
           ' \nТеперь с чистой совестью проходи /start'


class admin(Enum):
    Dav = 287157997
