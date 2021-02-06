User registration
=================



The main tool to work with objects in telebot is handlers. The body of the bot fully consists of this 'modules'. 


Message handler could have special input parameter::

 @bot.message_handler(commands=['str'])

It means that this handler will be called when user send::

  /str

Or you could choose what type of object will activate the handler::

  @bot.message_handler(content_types=['text'])
  
Main body of handler consists of functions.

Example::
   
 @bot.message_handler(commands=['start'])
 
   def first_func(msg):

      code...

   def secnd_func(msg):
 
      code... 
   
To go to the next function in handler you need to use::

  bot.register_next_step_handler(msg, func_name) 
  
Example::

  @bot.message_handler(commands=['start'])
	
   def first(msg):
	 
       code...
	   
       bot.register_next_step_handler(msg, second) 
	 
   def second(msg):
	 
       code...
   

.. note:: msg - is new message, wich user send after the first message .

Plot of the dialoge:
-----------------------

  1) User send message,wich triggers start handler
  
  2) Activated handler changes user start to enter the registration
  
  Loop:
  
    3) User answer for his  question
  
    4) His message activate next registration step
  
    5) Handler changes user's state and user goes to the next registration step

  End loop
  
  6) if user tap on special mistake inline button, callback comes from user
   
  7) Callback triggers callback handler, wich delete previous mistakes and ask question again
  
  8) if all right, user confirm registration by tapping on inline button

  9) callback from last step calls function wich sends inserts querry to database 
  
  
To determine any caused error there is checking structure before any registration message handler. If randomed flag_reg_start value it not equal to the user's value in Vedis db, it means that bot had an error and it was rebooted::

 import random 
 flag_reg_start = random.uniform(0, 20)

  
Plot of error:
--------------
 
  1) Bot have been rebooted during registration
  
  2) Any user action activate next handler
  
  3) Handler check user's flag_to_restart value
  
  4) If this value and generated in current session value are not equal, handler change user's state to 'Start' and send him to the start
  
.. warning:: If bot has been rebooted, user would not be able to continue previous registration. He has to start it again. 
 

.. note:: To prevent any problems start handler will work only in case when user send message to the bot for the first time or he is already in database . It works because of cheking user status and reboot indicator.


Starting the dialoge
-------------------- 

To start using platform user enter command  in the chat with bot::

  /start

Start handler::

   @bot.message_handler(commands=['start'])
   def start_message(msg):
     if dbworker.get_state(msg.chat.id) == config.States.S_START.value or dbworker.get_state(
            msg.chat.id) == config.States.S_ENTER_RiGHT.value or dbworker.get_state(
        msg.chat.id) is None:
        
        if func.in_base(msg): 
		# if user is in  Postgresql database
            if func.work_type(msg,0):
			# finding user work status 
                  
				  some code...
				  bot.register_next_step_handler(msg, login)
    
    def login(msg):
	  some code


More information about Postgresql functions here:

.. toctree::
   :maxdepth: 2
  
   psql_func
  

To change create and change variables related to user, need to use functions from file dbworker::

   dbworker.set_var(msg.chat.id, 'flag_reg_start', flag_reg_start)
   #changing variable value related to person
   
   dbworker.get_var(msg.chat.id, 'mes_to_del'))
   # getting variable value related to person
   
   dbworker.set_state(msg.chat.id, config.States.S_ENTER_NAME.value)
   # changing use's state	
	
   bworker.get_state(msg.chat.id)
   # getting usrs's state

For more information about Vedis fuctions read here:

.. toctree::
   :maxdepth: 2

   vedis_func
   
Handler from registration start,where Vedis function are used::

  @bot.message_handler(commands=['reg'])
  def start_message1(msg):
    
    dbworker.set_none(msg.chat.id)
    if not func.in_base(msg):
	 # using function with querry to check wether user is in database
        global flag_reg_start
		# indicator of error

        dbworker.set_var(msg.chat.id, 'flag_reg_start', flag_reg_start)
		#saving restart flag value 

        dbworker.set_var(msg.chat.id, 'Username', msg.from_user.username)
		#saving username

        dbworker.set_var(msg.chat.id, 'Chatid', msg.chat.id)
		# saving user's chat.id

         code...       
	   
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_NAME.value)
		# changing user's state to enter the next message handler

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
		# saving message to delete
	
	
Next steps are very similar, they differ from each other only with asking questions::

 @bot.message_handler(
    func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_MIDDLE.value and isinstance(msg.text,
                                                                                                          str))
	# lambda function plays 'if' construction role
	# if it returns false, message handler will not enter user
   def Family(msg):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'): 
	# determining the restart flag variable with user's chat.id

        dbworker.set_var(msg.chat.id, 'Name', msg.text) 
		# saving previous answer

        mes = bot.send_message(msg.chat.id, text=config.Questions.Middle.value, reply_markup=Kname)
		# question to user
        try:
            bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'mes_to_del'))
			#deleting previous question
        except Exception:
            pass
        dbworker.set_state(msg.chat.id, config.States.S_ENTER_FAMILY.value)
		# changing user state to enter next handler

        dbworker.set_var(msg.chat.id, 'mes_to_del', mes.message_id)
        dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)
    else:
        dbworker.set_state(msg.chat.id, config.States.S_START.value)
		# changing user's state
        bot.send_message(msg.chat.id, 'ой, видимо что-то пошло не так, пройди регистрацию заново', reply_markup=Keyreg)
		# bor reboot flag


If user did a mistake, he could go to previous step. This works with help of inline buttons. In bot method, were he send message to user, is also given parameter  reply_markup, where Keyreg is special buttons.

To use them need to create above all code inline keyboard::
  
  Kname = types.InlineKeyboardMarkup()
  Name_button = types.InlineKeyboardButton(text=buttom_text_string, callback_data=callback_string)
  Kname.add(Name_button)
 
Where callback is special signal, wich is very useful. To work them create callback handler (like message handler). In this project created callback handlers wich work with inline buttons.

Exampe::

 @bot.callback_query_handler(func=lambda call: True)
  def callback_querry(call):
    global flag_reg_start
    if str(flag_reg_start) == dbworker.get_var(call.message.chat.id, 'flag_reg_start'):
	@reboot flag
        if call.data == "yes" and dbworker.get_var(call.message.chat.id, 'flag_stop') != 'False':
		# main gate to the callback handler
            dbworker.set_var(call.message.chat.id, 'flag_stop', 'True')
			# rejecting to person second tap
            try:
                bot.delete_message(call.message.chat.id, dbworker.get_var(call.message.chat.id, 'mes_to_del'))
				#deleting previous message
            except Exception:
                pass
            func.insert_new(call.message)
			#inserting new user's personal data
            dbworker.set_none(call.message.chat.id)
			# creating variables for new user


After registration user chooses role. In this project roles are:

   1) 0 - None
   2) 1 - organizator
   3) 2 - participant
   
More information abut roles here:

.. toctree::
   :maxdepth: 2
  
   role_choosing
  
.. note:: You can choose organizator or participant role only once !

Fixing errors
-------------

There is some interesting bug, caused in this project by telebot architecture.

If during registration user did a mistake , he will tap on inline button 'mistake' and go to the previous step. But in fact because of human factor user can tap on that button twice or more before it will be deleted. As a result same callback handler will be actived more then once and ,therefore , callback body cody will run several times wich is absolutely incorrect.

To solve this issue need to change user's state immediately in the start of callback handler body and make a state check construction::

    elif call.data == 'family' and dbworker.get_state(call.message.chat.id) != config.States.S_ENTER_GROUP.value:
	#checking user's state value
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_GROUP.value)
			#changing user's state value
			some code...
   
As a result, user's state changes immediately and person is not able to call callback handler again in small time interval.


Deleting messages
-----------------


Every message or call handler have same deleting frame::

    try:
            bot.delete_message(msg.chat.id, dbworker.get_var(msg.chat.id, 'str'))
    except Exception:
             pass
    dbworker.set_var(msg.chat.id, 'str', mes.message_id)

Furthemore message handler have one extra line to save user's message::
   
   dbworker.set_var(msg.chat.id, 'user_wrong', msg.message_id)

where str could be:

 1) mes_to_del - bot question
 2) user_wrong - user's answer
 3) last_key_mes - bot second message on 'phone' step
 4) mes_to_del2 - bot second message during cheking out


Phone and date handlers habe one unique feature.
 
On their step user can give a lot of variants of answers. To delete all incorrect messages need to create new text handler which will save all their id::

 @bot.message_handler(content_types=['text'],
                     func=lambda msg: dbworker.get_state(msg.chat.id) == config.States.S_ENTER_DATE.value)
   def wrong_phone(msg):
    global flag_reg_start
     if str(flag_reg_start) == dbworker.get_var(msg.chat.id, 'flag_reg_start'):
        mes = bot.send_message(msg.chat.id, 'Нажми на кнопку в доп. клавиатуре')
        i = dbworker.get_var(msg.chat.id, 'len')
        dbworker.set_var(msg.chat.id, i, mes.message_id)
        dbworker.set_var(msg.chat.id, str(int(i) + 1), msg.message_id)
        dbworker.set_var(msg.chat.id, 'len', str(int(i) + 2))

When user give correct answer need to delete wrong messages. It wolud be done on next steps from phone and date. 

It means that next handlers (BDate and VKurl) need to have loops::

        if int(dbworker.get_var(msg.chat.id, 'len')) > 0:
            i = 0
            while i < int(dbworker.get_var(msg.chat.id, 'len')):
                try:
                    bot.delete_message(msg.chat.id, int(dbworker.get_var(msg.chat.id, str(i))))
                except Exception:
                    pass
                i += 1
				
				
	
