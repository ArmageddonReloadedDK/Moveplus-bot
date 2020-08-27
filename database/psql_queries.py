import psycopg2

from settings import config
from database import vedis_queries

connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()

bot = config.get_bot()


def get_db_connection():
    return connection


def in_base(msg):
    cursor.execute(
        '''select p.p_id from public.ev_people p where p.chat_id='%s' ''' % (msg.chat.id))
    rows_info = cursor.fetchall()
    if len(rows_info) > 0:
        return True
    else:
        return False


def inform_state(msg):
    cursor.execute(
        '''select p.chat_id from ev_people p, spec s where p.p_id=s.spec_id and s.inform=TRUE and p.chat_id='%s' ''' % (
            msg.chat.id))
    rows_info = cursor.fetchall()
    if len(rows_info) > 0:
        return True
    else:
        return False


def work_type(msg, x):
    cursor.execute(
        '''select p.p_id from ev_people p where p.chat_id='%s' and p.status='%s' ''' % (msg.chat.id, x))
    rows_info = cursor.fetchall()
    if len(rows_info) > 0:
        return True
    else:
        return False



def reg_type(msg):
    cursor.execute(
        '''select o.regist from ev_people p,organizators o where p.chat_id='%s' and o.org_id=p.p_id and p.status='%s' ''' % (
        msg.chat.id, 1))
    rows = cursor.fetchall()
    return rows[0][0]


def insert_new(msg):
    cursor.execute(
        ''' insert into public.ev_people (first_name, middle_name, family_name, group_name, phone, telegram_username,   birth_date, status, vk_url, chat_id)
         values('%s','%s','%s','%s',%s,'%s','%s',default ,'%s','%s')''' % (
            vedis_queries.get_var(msg.chat.id, 'Name'), vedis_queries.get_var(msg.chat.id, 'Middle'),
            vedis_queries.get_var(msg.chat.id, 'Family'), vedis_queries.get_var(msg.chat.id, 'Group'),
            vedis_queries.get_var(msg.chat.id, 'Phone'), vedis_queries.get_var(msg.chat.id, 'Username'),
            vedis_queries.get_var(msg.chat.id, 'Date'), vedis_queries.get_var(msg.chat.id, 'VK'),
            vedis_queries.get_var(msg.chat.id, 'Chatid')))
    connection.commit()

def registraion_change(status,chat_id):
    cursor.execute(
        ''' update organizators set regist='%s' where org_id=(select p.p_id from ev_people p where p.chat_id='%s') ''' % (status,
            chat_id))
    connection.commit()
