import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "مرحباً جاسر! 🚀\nأرسل الـ ID الآن:")
    bot.register_next_step_handler(msg, process_id_step)

def process_id_step(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, "تمام، أرسل كلمة السر (Password):")
    bot.register_next_step_handler(msg, process_password_step, user_id)

def process_password_step(message, user_id):
    password = message.text
    bot.send_message(message.chat.id, "⌛ جاري محاولة الدخول... انتظر ثواني.")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10) # انتظر حتى 10 ثوانٍ لظهور العناصر
    
    try:
        driver.get("https://m.facebook.com")
        
        # البحث عن حقل الإيميل وإدخاله
        email_field = wait.until(EC.presence_of_element_status((By.NAME, "email")))
        email_field.send_keys(user_id)
        
        # البحث عن حقل الباسورد وإدخاله (استخدام الاسم مباشرة)
        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.send_keys(password)
        
        # الضغط على زر تسجيل الدخول
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        
        time.sleep(7) # وقت كافٍ للتحميل بعد الضغط
        
        bot.send_message(message.chat.id, f"🔗 الرابط الحالي: {driver.current_url}")
        
        driver.save_screenshot("result.png")
        with open("result.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="📸 لقطة شاشة لنتيجة العملية")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ في العثور على العناصر: {str(e)[:100]}")
    finally:
        driver.quit()

print("البوت يعمل...")
bot.infinity_polling()
