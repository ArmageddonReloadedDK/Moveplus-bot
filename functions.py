import psycopg2
import telebot
import config
connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="123",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()

bot = telebot.TeleBot(config.token)
def here(msg):
    cursor.execute(
        '''select p.chat_id from people p, spec s where p.p_id=s.spec_id and s.inform=TRUE and p.chat_id='%s' '''%(msg.chat.id))
    rows_info = cursor.fetchall()
    if len(rows_info)>0:
            return True
    else:
            return False
def type(msg,x):
    cursor.execute(
        '''select p.p_id from people p where p.chat_id='%s' and p.work_status='%s' '''%(msg.chat.id,x))
    rows_info = cursor.fetchall()
    if len(rows_info)>0:
            return True
    else:
            return False

def no_permis(msg):
            bot.send_message(msg.chat.id, 'Эээ, куда \n Недостаточно прав')

def reg_type(msg):
    cursor.execute(
        '''select p.regist from people p where p.chat_id='%s' and p.work_status='%s' '''%(msg.chat.id,1))
    rows = cursor.fetchall()
    return rows[0][0]



