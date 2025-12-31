import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# إعدادات التلجرام الخاصة بك
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def run_fb_simulator(chat_id, user_id, password):
    bot.send_message(chat_id, "⏳ جاري تشغيل المحاكي (Selenium) وفحص الحساب...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # تعريف المتصفح
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://m.facebook.com")
        time.sleep(3)
        
        # البحث عن حقول الإدخال وإرسال البيانات
        driver.find_element(By.NAME, "email").send_keys(user_id)
        driver.find_element(By.NAME, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        
        time.sleep(7) # انتظار التحميل بعد الضغط
        
        # استخراج النتائج
        current_url = driver.current_url
        page_html = driver.page_source[:1500] # نأخذ جزء فقط بسبب قيود حجم رسالة تلجرام
        
        bot.send_message(chat_id, f"✅ تم الانتهاء!\n🔗 الرابط الحالي: {current_url}")
        bot.send_message(chat_id, f"📄 جزء من HTML:\n\n", parse_mode="Markdown")
        
        # لقطة شاشة للنتيجة
        driver.save_screenshot("result.png")
        with open("result.png", "rb") as photo:
            bot.send_photo(chat_id, photo, caption="📸 لقطة شاشة لصفحة النتيجة بعد تسجيل الدخول")

    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ أثناء المحاكاة: {str(e)}")
    finally:
        driver.quit()

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "مرحباً جاسر! أرسل لي الـ ID (الإيميل) الخاص بالفيسبوك:")
    bot.register_next_step_handler(msg, get_id)

def get_id(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, f"تم استقبال ID: {user_id}\nالآن أرسل الباسورد:")
    bot.register_next_step_handler(msg, get_pass, user_id)

def get_pass(message, user_id):
    password = message.text
    bot.send_message(message.chat.id, "🚀 بدأنا العمل.. انتظر ثواني.")
    run_fb_simulator(message.chat.id, user_id, password)

print("Bot is running...")
bot.polling()
