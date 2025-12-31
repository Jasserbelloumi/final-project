import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def send_as_file(chat_id, driver, caption):
    """التقاط الشاشة وإرسالها كملف مضغوط لضمان الفتح"""
    try:
        path = f"step_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            bot.send_document(chat_id, f, caption=caption)
        time.sleep(1.5) # وقت كافٍ للرفع قبل الحذف
        if os.path.exists(path): os.remove(path)
    except Exception as e:
        print(f"Error: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "🚀 بدأنا العمل بنظام الملفات.\nأرسل الـ ID:")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "تمام، أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري التشغيل.. ستصلك الخطوات كملفات.")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument('user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36')
    
    driver = webdriver.Chrome(options=opts)

    try:
        # الدخول لنسخة فيسبوك الخفيفة
        driver.get("https://free.facebook.com/login.php")
        time.sleep(3)
        send_as_file(message.chat.id, driver, "1- صفحة البداية")

        # إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        send_as_file(message.chat.id, driver, "2- إدخال البيانات")

        # محاولة الضغط بطريقة آمنة
        try:
            login_btn = driver.find_element(By.NAME, "login")
            login_btn.click()
        except:
            # إذا لم يجد الزر، يبحث عن أي زر submit ويضغط عليه
            btns = driver.find_elements(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
            if btns: btns[0].click()
        
        time.sleep(8)
        
        # النتيجة النهائية
        bot.send_message(message.chat.id, f"🏁 الرابط النهائي: {driver.current_url}")
        send_as_file(message.chat.id, driver, "3- لقطة الشاشة النهائية")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:100]}")
    finally:
        time.sleep(2)
        driver.quit()

bot.infinity_polling()
