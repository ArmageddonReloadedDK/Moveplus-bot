from algorythms import main
from base.base_human import Base_human_class
from settings import config


class Family_search_class(Base_human_class):

    def __init__(self):
        super().__init__()

    def family_search_step_0(self, msg):
        if self.work_type(msg, 1):
            self.bot.send_message(msg.chat.id, 'Введите фамилию человека, которого нужно найти ')
            return True

        else:
            main.no_permis(msg)
            return False

    def family_search_step_1(self, msg):
        try:
            a = str(msg.text)
            a.capitalize()
            self.cursor.execute(
                ''' select * from ev_people r where (select similarity(r.family_name,'%s'))>0.3 ''' % (
                    a))
            rows = self.cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.bot.send_message(msg.chat.id,
                                          f' Личный номер: {row[0]}\n{row[3]} {row[2]} {row[1]} \nНомер телефона: {row[4]}\nГруппа {row[6]}\nНомер комнаты: {row[5]}')
            else:
                self.bot.send_message(msg.chat.id, 'такого человека нет')
        except Exception:
            self.bot.send_message(msg.chat.id, 'ошибка в фамимлии')



