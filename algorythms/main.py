from settings import config

bot=config.get_bot()

def no_permis(msg):
    bot.send_message(msg.chat.id, 'Эээ, куда \n Недостаточно прав')


def state(x):
    if x == 0:
        return 'Не прибыл'
    if x == 1:
        return 'Прибыл'
    if x == 2:
        return 'Покинул'
