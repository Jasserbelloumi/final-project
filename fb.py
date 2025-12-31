import telebot
import os

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ أهلاً جاسر! البوت شغال الآن على سيرفر GitHub وجاهز لاستلام الحسابات.")

print("جاري تشغيل البوت...")
bot.infinity_polling()
