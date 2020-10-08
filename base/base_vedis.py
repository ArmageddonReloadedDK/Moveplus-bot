from vedis import Vedis
from settings.config import db_file
import datetime

class base_vedis_class():
    def get_state(self,user_id):
        with Vedis(db_file) as db:
          try:
            c = db[user_id].decode()
            return c
          except Exception:
            return None


    def set_state(self,user_id, value):
        with Vedis(db_file) as db:
            try:

                db[user_id] = value

            except Exception:
                return False

    @classmethod
    def get_var(cls,user_id, var):
        with Vedis(db_file) as db:
           try:
             c = db[str(user_id) + var].decode()
             return c
           except Exception:
               return False


    def set_var(self,user_id, var, value):
        with Vedis(db_file) as db:
            try:

                db[str(user_id) + var] = value
                c = db[str(user_id) + var].decode()
                return c

            except Exception:
                return False


    def set_none(self,user_id):
        global a
        with Vedis(db_file) as db:

                db[str(user_id) + 'Name'] = 0
                db[str(user_id) + 'Middle'] = 0
                db[str(user_id) + 'Family'] = 0
                db[str(user_id) + 'Group'] = 0
                db[str(user_id) + 'Date'] = 0
                db[str(user_id) + 'VK'] = 0
                db[str(user_id) + 'Chatid'] = 0
                db[str(user_id) + 'Username'] = 0
                db[str(user_id) + 'Phone'] = 0
                db[str(user_id) + 'flag_stop'] = 0
                db[str(user_id) + 'len'] = 0



    def validate(self,date_text):
        try:
            datetime.datetime.strptime(date_text, '%d.%m.%Y')
            return True
        except ValueError:
            return False
