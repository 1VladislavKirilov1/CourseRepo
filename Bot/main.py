import telebot
from config import keys, TOKEN
from extensions import APIException, Convertor
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую!\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n{e}')
    else:
        bot.reply_to(message, answer)

bot.polling()

