from algorythms import main
from base.base_human import Base_human_class


class Regchange(Base_human_class):
    def __init__(self):
        super().__init__()



    def registraion_change_step_0(self,msg):
        if self.work_type(msg, 1):
            if not self.reg_type(msg) or self.reg_type(msg) is None:
                self.registraion_change(True, msg.chat.id)
                self.bot.send_message(msg.chat.id, 'Режим GO.\nСтатус изменен. Вы можете выселять людей')

            else:
                self.registraion_change(False, msg.chat.id)
                self.bot.send_message(msg.chat.id, 'Режим GO.\nСтатус изменен. Вы НЕ можете выселять людей ')
        else:
            main.no_permis(msg)

    def checkOut(self,msg):
        if self.work_type(msg, 1):
            if not self.check_type(msg) or self.check_type(msg) is None:
                self.check_out_change(True, msg.chat.id)
                self.bot.send_message(msg.chat.id, 'Стойка регистрации.\nСтатус изменен. Вы можете выселять людей')

            else:
                self.check_out_change(False, msg.chat.id)
                self.bot.send_message(msg.chat.id, 'Стойка регистрации.\nСтатус изменен. Вы НЕ можете выселять людей ')
        else:
            main.no_permis(msg)