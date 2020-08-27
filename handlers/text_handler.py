import telebot
from settings.config import token

############################################
#
# Создание клавиатур
#
Menu = telebot.types.ReplyKeyboardMarkup(True, True)
Menu.row('Карта ', 'Расписание')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Аниме на аве', 'Вилку в глаз или не вилку в глаз ?')

#############################################

bot = telebot.TeleBot(token)


def main_text_handler(msg):
    if 'Аниме на аве' in msg.text:
        bot.send_message(msg.chat.id, 'Здоровья маме')

    elif 'Вилку в глаз или не вилку в глаз ?' in msg.text:
        bot.send_message(msg.chat.id, 'Я смотрю, ты не одноглазый')

    elif 'Я сладкий пирожочек' in msg.text:
        bot.send_message(msg.chat.id, 'Ну ладно, тебе прощаю')

    elif 'Я не Саня' in msg.text:
        bot.send_message(msg.chat.id, 'А кто тогда Саня, Я ? Жду сотку', reply_markup=keyboard1)
    elif 'Жилье' in msg.text:
        bot.send_message(msg.chat.id, 'Жилье')
    elif 'Карта' in msg.text:
        photo = open('images/map.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Ночные точки' in msg.text:
        photo = open('images/play.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Расписание' in msg.text:
        photo = open('images/schedule.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    elif 'Нужна мед помощь' in msg.text:
        photo = open('images/schedule.jpg', 'rb')
        bot.send_photo(msg.chat.id, photo)
        bot.send_message(msg.chat.id, 'Переход в основное меню', reply_markup=Menu)
    else:
        bot.send_message(msg.chat.id, 'Нужен набор доступных команд ?Держи: ')
