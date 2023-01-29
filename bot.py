from decouple import config
from telebot import types
import telebot
from product.models import Product

bot = telebot.TeleBot(config('TOKEN'))
print(Product.objects.all())

@bot.message_handler(commands=['start'])
def get_message(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Показать товары aliOP!')
    markup.add(btn1)

    bot.send_message(chat_id, text="Привет, {0.first_name}! Я бот для aliOP".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala (message):
    print(message.text)
    chat_id = message.chat.id


# bot.polling(none_stop=True)

