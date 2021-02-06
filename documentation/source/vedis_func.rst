Vedis database methods
======================

Importing mosules::

 from vedis import Vedis
 import config
 import datetime
 

.. note:: Vedis database return always string values

.. important:: Here we use user's chat.id as Primary key

You see some function there are try except construction. It is necessary because we can not garantuee primary key value existance due to human aspect.

Getting user's state::

  def get_state(user_id):
    with Vedis(config.db_file) as db:
      try:
        c = db[user_id].decode()
        return c
      except Exception:
        return None

Setting user's state::

 def set_state(user_id, value):
    with Vedis(config.db_file) as db:
            db[user_id] = value

Getting personal variable::

 def get_var(user_id, var):
    with Vedis(config.db_file) as db:
       try:
         c = db[str(user_id) + var].decode()
         return c
       except Exception:
           return None

Setting personal variable::

 def set_var(user_id, var, value):
    with Vedis(config.db_file) as db:
            db[str(user_id) + var] = value


Setting all variable to default values::

 def set_none(user_id):
    with Vedis(config.db_file) as db:

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


Function to check entered date::

 def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False
