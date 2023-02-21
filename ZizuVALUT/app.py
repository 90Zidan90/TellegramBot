import telebot

from config import keys, TOKEN
from extensions import ConvertionException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Приветствую тебя,дорогой друг, {message.from_user.first_name}!\nХотите узнать сколько валюты в другой? ' \
           f' \nТогда введите название валюты и колличество по следующей схеме :\n<имя вылюты>\
<в какую валюту перевести>\<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Не правильный запрос.\nСлишком много параметров.')

        quote, base, amount = values
        total_base = СurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\т{e}')
    else:
        text = f'Цена {amount} {quote} в  {base} : {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
