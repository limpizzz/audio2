import telebot
from config import token
from voicehandler import handle_voice_message

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "привет!) Отправьте голосовое сообщение командой /stt для расшифровки.")


@bot.message_handler(commands=['stt'])
def stt(message):
    msg = bot.send_message(message.chat.id, "отправь голосовое сообщениееее.")
    bot.register_next_step_handler(msg, handle_voice_message, bot)


bot.polling()