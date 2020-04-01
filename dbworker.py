from vedis import Vedis
import config
import datetime
import sqlite3



def get_state(user_id):
    with Vedis(config.db_file) as db:
      try:
        c = db[user_id].decode()
        return c
      except Exception:
        return None


def set_state(user_id, value):
    global a
    with Vedis(config.db_file) as db:
        try:

            db[user_id] = value

        except Exception:
            return False


def get_var(user_id, var):
    with Vedis(config.db_file) as db:
       try:
         c = db[str(user_id) + var].decode()
         return c
       except Exception:
           return False


def set_var(user_id, var, value):
    global a
    with Vedis(config.db_file) as db:
        try:

            db[str(user_id) + var] = value

        except Exception:
            return False


def set_none(user_id):
    global a
    with Vedis(config.db_file) as db:
        try:

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



        except Exception:
            return False


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False
