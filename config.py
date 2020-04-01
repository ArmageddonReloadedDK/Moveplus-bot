from enum import Enum

token = '616126274:AAGlRipQWcuwhgHdd83ThFvKchNfrf9ybqA'
db_file = "database.vdb"
db_vars = "varbase.vdb"


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
    S_busy='11'
    S_busy_org = '13'
    S_not_busy='12'



class Questions(Enum):
    Name = 'Как тебя зовут ?'
    Middle = 'Какая у тебя фамилия?'
    Family = 'А отчество (при наличии)?'
    Phone = 'Дальше нужен номер телефона\n(Нажми на кнопку в доп меню)'
    PhoneQ = '(чтобы мы смогли с тобой связаться)'
    Group = 'Теперь подскажи группу, в которой ты учишься.\n (Осталось совсем немного)'
    Date = 'Дальше - дата рождения в формате xx.xx.xxxx'
    Vk = 'И последнее. Скинь ссылку на твой вк'
    Stop = 'От души. Надеюсь, ты не ошибся(-лась) нигде. Но если ошибся(-лась) -\n тебе сюда @ArmageddonReloaded. \nТеперь с чистой совестью проходи /start'

class admin(Enum):
    Dav=287157997
