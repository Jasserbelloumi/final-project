import telebot
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def send_file(chat_id, driver, caption):
    try:
        path = f"iphone_capture_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            bot.send_document(chat_id, f, caption=caption)
        time.sleep(1)
        if os.path.exists(path): os.remove(path)
    except: pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🍏 جاري محاكاة بيئة iPhone 14 Pro Max كاملة...")
    process_login(message, "61583389620613", "jasser vodka")

def process_login(message, uid, pas):
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    # بصمة آيفون حقيقية 100%
    ua = "Mozilla/5.0 (iPhone15,3; U; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1"
    opts.add_argument(f'user-agent={ua}')
    
    # ضبط أبعاد الشاشة لتطابق الآيفون
    opts.add_argument("--window-size=430,932") 
    
    driver = webdriver.Chrome(options=opts)
    
    try:
        # الدخول للرابط m وليس free لضمان استجابة شكل الآيفون
        driver.get("https://m.facebook.com/")
        time.sleep(5)
        send_file(message.chat.id, driver, "📱 شاشة الآيفون الافتتاحية")

        # كتابة البيانات ببطء شديد
        driver.find_element(By.NAME, "email").send_keys(uid)
        time.sleep(random.uniform(1, 2))
        driver.find_element(By.NAME, "pass").send_keys(pas)
        time.sleep(random.uniform(1, 2))
        
        send_file(message.chat.id, driver, "✍️ تم ملء البيانات (نمط آيفون)")

        # الضغط على زر الدخول
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
        
        bot.send_message(message.chat.id, "⏳ تم الضغط.. ننتظر استجابة سيرفرات فيسبوك.")
        time.sleep(15) # زيادة وقت الانتظار للأمان
        
        send_file(message.chat.id, driver, f"🏁 الحالة النهائية\nالرابط: {driver.current_url}")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث تعطل: {str(e)[:100]}")
    finally:
        driver.quit()

bot.infinity_polling()
