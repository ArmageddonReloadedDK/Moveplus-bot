# Telegram-event-registration-bot
Specific telegram bot which provides event registration process. In the end of the dialog the bot sends queries to local host postgresql database. Also to configure user state bot uses Vedis file-database.

How it works:
To make registration dialog possible, every time,when user give information about himself, bot changes state-variable in Vedis database. Then, next message-handler compares user state-variable and variable, wich is constant to current handler. If it is tue, next handler again changes state-variable and starts to work with last user's messag.

This product was finished only with help of my testers-team. Thks to AC. :) 
