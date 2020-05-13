import psycopg2
import telebot
import config
import dbworker
connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="123",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()

bot = telebot.TeleBot(config.token)

def in_base(msg):
    cursor.execute(
        '''select p.p_id from public.ev_people p where p.chat_id='%s' '''%(msg.chat.id))
    rows_info = cursor.fetchall()
    if len(rows_info)>0:
            return True
    else:
            return False

def inform_state(msg):
    cursor.execute(
        '''select p.chat_id from ev_people p, spec s where p.p_id=s.spec_id and s.inform=TRUE and p.chat_id='%s' '''%(msg.chat.id))
    rows_info = cursor.fetchall()
    if len(rows_info)>0:
            return True
    else:
            return False

def work_type(msg,x):
    cursor.execute(
        '''select p.p_id from ev_people p where p.chat_id='%s' and p.status='%s' '''%(msg.chat.id,x))
    rows_info = cursor.fetchall()
    if len(rows_info)>0:
            return True
    else:
            return False

def no_permis(msg):
            bot.send_message(msg.chat.id, 'Эээ, куда \n Недостаточно прав')

def reg_type(msg):
    cursor.execute(
     '''select o.regist from ev_people p,organizators o where p.chat_id='%s' and o.org_id=p.p_id and p.status='%s' '''%(msg.chat.id,1))
    rows = cursor.fetchall()
    return rows[0][0]

def insert_new(msg):
    cursor.execute(
        ''' insert into public.ev_people (first_name, middle_name, family_name, group_name, phone, telegram_username,   birth_date, status, vk_url, chat_id)
         values('%s','%s','%s','%s',%s,'%s','%s',default ,'%s','%s')''' % (
            dbworker.get_var(msg.chat.id, 'Name'), dbworker.get_var(msg.chat.id, 'Middle'),
            dbworker.get_var(msg.chat.id, 'Family'), dbworker.get_var(msg.chat.id, 'Group'),
            dbworker.get_var(msg.chat.id, 'Phone'), dbworker.get_var(msg.chat.id, 'Username'),
            dbworker.get_var(msg.chat.id, 'Date'), dbworker.get_var(msg.chat.id, 'VK'),
            dbworker.get_var(msg.chat.id, 'Chatid')))
    connection.commit()
def state(x):
    if x==0:
        return 'Не прибыл'
    if x==1:
        return 'Прибыл'
    if x==2:
        return 'Покинул'



