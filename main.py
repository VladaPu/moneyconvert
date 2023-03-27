import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Здравствуйте! \n Для перевода валюты введите свой запрос в формате:\n" \
           "{валюта, из которой вы хотите перевести} {валюта, в которую вы хотите перевести} {сумма для перевода}\n" \
           "Чтобы увидеть список доступных валют, введите команду /values"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        base, sym, amount = values
        answer = Convertor.get_price(base, sym, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
