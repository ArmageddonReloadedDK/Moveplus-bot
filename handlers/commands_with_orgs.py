from database import psql_queries
from database import vedis_queries
from settings import config
import telebot
import psycopg2
from handlers import algorythms

bot=config.get_bot()

connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()


class status_change():

        @staticmethod
        def step_0(msg):

                if psql_queries.inform_state(msg) and psql_queries.work_type(msg, 1):
                    bot.send_message(msg.chat.id, 'Введи номер человека, у которого нужно изменить статус привилегий')
                    return True
                else:
                    algorythms.no_permis(msg)
                    return False

        @staticmethod
        def step_1(msg):
            try:
                a = int(msg.text)
                cursor.execute(''' select p.chat_id from ev_people p where p.p_id='%s' ''' % (int(msg.text)))
                rows = cursor.fetchall()
                if rows[0][0] == config.admin.Dav.value:
                    bot.send_message(msg.chat.id, 'Сейчас бы главному админу менять статус')
                else:
                    cursor.execute(''' select * from spec s where s.spec_id='%s' ''' % (a))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        bot.send_message(msg.chat.id, 'Какой статус ? True-1/False-0')
                        vedis_queries.set_var(msg.chat.id, 'cname', msg.text)
                        return True
                    else:
                        bot.send_message(msg.chat.id, 'такого человека нет')
                        return False
            except Exception:
                bot.send_message(msg.chat.id, 'ошибка в номере')
                return False

        @staticmethod
        def step_2(msg):
            if '1' in msg.text:
                cursor.execute(
                    ''' update spec set inform=TRUE where spec_id='%s' ''' % (vedis_queries.get_var(msg.chat.id, 'cname')))
                connection.commit()
                bot.send_message(msg.chat.id, 'Статус обвнолен. Для выведения списка спец лиц введите /list')
            elif '0' in msg.text:
                cursor.execute(
                    ''' update spec set inform=FALSE where spec_id='%s' ''' % (vedis_queries.get_var(msg.chat.id, 'cname')))
                connection.commit()
                bot.send_message(msg.chat.id, 'Статус обвнолен. Для выведения списка спец лиц введите /list')


class Write_to_person():

    @staticmethod
    def step_0(msg):
        if psql_queries.work_type(msg, 1):
            bot.send_message(msg.chat.id, 'Введи номер человека, кому нужно написать ')
            return True
        else:
            algorythms.no_permis(msg)
            return False

    @staticmethod
    def step_1(msg):
        vedis_queries.set_var(msg.chat.id, 'pwrite', msg.text)
        bot.send_message(msg.chat.id, 'Что написать ему ?')

    @staticmethod
    def step_2(msg):
        try:
            a = int(vedis_queries.get_var(msg.chat.id, 'pwrite'))
            cursor.execute(''' select chat_id from ev_people p where p_id='%s' ''' % (a))
            rows = cursor.fetchall()
            if len(rows) > 0:
                bot.send_message(rows[0][0], msg.text)
                bot.send_message(msg.chat.id, 'Доставлено')
            else:
                bot.send_message(msg.chat.id, ' Такого человека нет')
        except Exception:
            bot.send_message(msg.chat.id, ' Такого человека нет')

class Regchange():
    @staticmethod
    def step_0(msg):
        if psql_queries.work_type(msg, 1):
            if not psql_queries.reg_type(msg) or psql_queries.reg_type(msg) is None:
                psql_queries.registraion_change(True, msg.chat.id)
                bot.send_message(msg.chat.id, 'Статус изменен на True. Вам будут приходить заявки о выселении')

            else:
                psql_queries.registraion_change(False, msg.chat.id)
                bot.send_message(msg.chat.id, 'Статус изменен на False. Заявки больше не будут приходить ')
        else:
            algorythms.no_permis(msg)
