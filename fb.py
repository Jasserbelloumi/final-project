import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "مرحباً جاسر! 🚀\nمن فضلك أرسل الـ ID (الإيميل أو الهاتف):")
    bot.register_next_step_handler(msg, process_id_step)

def process_id_step(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, f"تم حفظ الـ ID: {user_id}\nالآن، أرسل كلمة السر (Password):")
    bot.register_next_step_handler(msg, process_password_step, user_id)

def process_password_step(message, user_id):
    password = message.text
    bot.send_message(message.chat.id, "⌛ جاري تشغيل المحاكي والدخول إلى فيسبوك... انتظر قليلاً.")
    
    # إعدادات المتصفح الخفي للعمل على GitHub Actions
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://m.facebook.com")
        time.sleep(3)
        
        # محاولة إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys(user_id)
        driver.find_element(By.NAME, "/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/form/div[1]/section/div/div[2]/div/div/div/div/div/div/input").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        
        time.sleep(7)
        
        # إرسال النتيجة
        bot.send_message(message.chat.id, f"🔗 الرابط الحالي بعد المحاولة: {driver.current_url}")
        
        # أخذ سكرين شوت للنتيجة
        driver.save_screenshot("result.png")
        with open("result.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="📸 لقطة شاشة لنتيجة الدخول")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)}")
    finally:
        driver.quit()

print("البوت قيد التشغيل الآن...")
bot.infinity_polling()
