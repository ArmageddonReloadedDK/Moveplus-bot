from algorythms import main
from base.base_human import Base_human_class
from settings import config


class Status_change(Base_human_class):
    def __init__(self):
        super().__init__()

    def status_change_step_0(self, msg):

        if self.inform_state(msg) and self.work_type(msg, 1):
            self.bot.send_message(msg.chat.id, 'Введи номер человека, у которого нужно изменить статус привилегий')
            return True
        else:
            main.no_permis(msg)
            return False

    def status_change_step_1(self, msg):
        try:
            a = int(msg.text)
            self.cursor.execute(''' select p.chat_id from ev_people p where p.p_id='%s' ''' % (int(msg.text)))
            rows = self.cursor.fetchall()
            if rows[0][0] == config.admin.Dav.value:
                self.bot.send_message(msg.chat.id, 'Сейчас бы главному админу менять статус')
            else:
                self.cursor.execute(''' select * from spec s where s.spec_id='%s' ''' % (a))
                rows = self.cursor.fetchall()
                if len(rows) > 0:
                    self.bot.send_message(msg.chat.id, 'Какой статус ? True-1/False-0')
                    self.set_var(msg.chat.id, 'cname', msg.text)
                    return True
                else:
                    self.bot.send_message(msg.chat.id, 'такого человека нет')
                    return False
        except Exception:
            self.bot.send_message(msg.chat.id, 'ошибка в номере')
            return False

    def status_change_step_2(self, msg):
        if '1' in msg.text:
            self.cursor.execute(
                ''' update spec set inform=TRUE where spec_id='%s' ''' % (self.get_var(msg.chat.id, 'cname')))
            self.connection.commit()
            self.bot.send_message(msg.chat.id, 'Статус обвнолен. Для выведения списка спец лиц введите /list')
        elif '0' in msg.text:
            self.cursor.execute(
                ''' update spec set inform=FALSE where spec_id='%s' ''' % (self.get_var(msg.chat.id, 'cname')))
            self.connection.commit()
            self.bot.send_message(msg.chat.id, 'Статус обвнолен. Для выведения списка спец лиц введите /list')
