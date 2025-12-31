import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def capture(chat_id, driver, text):
    """دالة محسنة لالتقاط الصور وضمان رفعها"""
    try:
        path = f"img_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            bot.send_photo(chat_id, f, caption=text[:100]) # تقصير النص لتجنب خطأ 400
        time.sleep(1) # وقت لضمان الرفع
        if os.path.exists(path): os.remove(path)
    except Exception as e:
        print(f"Error sending photo: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "🚀 البوت جاهز.\nأرسل الـ ID:")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري العمل.. انتظر الصور.")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36')
    
    driver = webdriver.Chrome(options=opts)

    try:
        driver.get("https://free.facebook.com/login.php")
        time.sleep(3)
        capture(message.chat.id, driver, "1- صفحة الدخول")

        driver.find_element(By.NAME, "email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        capture(message.chat.id, driver, "2- إدخال البيانات")

        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.execute_script("document.forms[0].submit();")
        
        time.sleep(8)
        # إرسال الرابط النهائي كنص منفصل لتجنب أخطاء الصور
        final_url = driver.current_url
        bot.send_message(message.chat.id, f"🔗 الرابط النهائي: {final_url}")
        capture(message.chat.id, driver, "3- النتيجة النهائية")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:50]}")
    finally:
        time.sleep(2) # انتظار أخير قبل الإغلاق
        driver.quit()

bot.infinity_polling()
