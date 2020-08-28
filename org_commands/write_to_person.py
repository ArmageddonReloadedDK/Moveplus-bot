from algorythms import main
from base.base_human import Base_human_class


class write_to_person(Base_human_class):
    def __init__(self):
        super().__init__()


    def write_to_person_step_0(self, msg):
        if self.work_type(msg, 1):
            self.bot.send_message(msg.chat.id, 'Введи номер человека, кому нужно написать ')
            return True
        else:
            main.no_permis(msg)
            return False

    def write_to_person_step_1(self, msg):
        self.set_var(msg.chat.id, 'pwrite', msg.text)
        self.bot.send_message(msg.chat.id, 'Что написать ему ?')

    def write_to_person_step_2(self, msg):
        try:
            a = int(self.get_var(msg.chat.id, 'pwrite'))
            self.cursor.execute(''' select chat_id from ev_people p where p_id='%s' ''' % (a))
            rows = self.cursor.fetchall()
            if len(rows) > 0:
                self.bot.send_message(rows[0][0], msg.text)
                self.bot.send_message(msg.chat.id, 'Доставлено')
            else:
                self.bot.send_message(msg.chat.id, ' Такого человека нет')
        except Exception:
            self.bot.send_message(msg.chat.id, ' Такого человека нет')
