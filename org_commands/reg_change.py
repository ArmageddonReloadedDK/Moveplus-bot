from algorythms import main
from base.base_human import Base_human_class


class Regchange(Base_human_class):
    def __init__(self):
        super().__init__()



    def registraion_change_step_0(self,msg):
        if self.work_type(msg, 1):
            if not self.reg_type(msg) or self.reg_type(msg) is None:
                self.registraion_change(True, msg.chat.id)
                self.bot.send_message(msg.chat.id, 'Статус изменен на True. Вам будут приходить заявки о выселении')

            else:
                self.registraion_change(False, msg.chat.id)
                self.bot.send_message(msg.chat.id, 'Статус изменен на False. Заявки больше не будут приходить ')
        else:
            main.no_permis(msg)
