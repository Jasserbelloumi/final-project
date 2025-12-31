import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

# إرسال رسالة تنبيه عند بدء التشغيل فوراً
try:
    bot.send_message("6998492040", "🚀 البوت يعمل الآن على GitHub ومتصل بنجاح!") 
except:
    print("برجاء التأكد من Chat ID أو التوكن")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً جاسر! أنا جاهز. أرسل الإيميل الآن:")
    bot.register_next_step_handler(message, get_id)

def get_id(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, "تمام، أرسل الباسورد الآن:")
    bot.register_next_step_handler(msg, get_pass, user_id)

def get_pass(message, user_id):
    password = message.text
    bot.send_message(message.chat.id, "⌛ جاري الدخول للمتصفح المحاكي...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://m.facebook.com")
        time.sleep(2)
        driver.find_element(By.NAME, "email").send_keys(user_id)
        driver.find_element(By.NAME, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        time.sleep(6)
        
        bot.send_message(message.chat.id, f"🔗 الرابط بعد المحاولة: {driver.current_url}")
        driver.save_screenshot("res.png")
        with open("res.png", "rb") as f:
            bot.send_photo(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ: {str(e)}")
    finally:
        driver.quit()

bot.infinity_polling()
