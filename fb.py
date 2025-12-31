import telebot
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def send_step_screenshot(chat_id, driver, caption):
    """دالة مساعدة لأخذ وإرسال لقطة شاشة"""
    filename = f"step_{int(time.time())}.png"
    driver.save_screenshot(filename)
    with open(filename, "rb") as photo:
        bot.send_photo(chat_id, photo, caption=caption)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "مرحباً جاسر! 🚀\nنظام التتبع بالصور مفعل.\nأرسل الـ ID الآن:")
    bot.register_next_step_handler(msg, process_id_step)

def process_id_step(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, "تمام، أرسل كلمة السر (Password):")
    bot.register_next_step_handler(msg, process_password_step, user_id)

def process_password_step(message, user_id):
    password = message.text
    bot.send_message(message.chat.id, "⌛ بدأنا العمل.. تابع الصور بالأسفل:")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # الخطوة 1: فتح الموقع
        driver.get("https://free.facebook.com/login.php")
        time.sleep(2)
        send_step_screenshot(message.chat.id, driver, "1️⃣ تم فتح صفحة تسجيل الدخول")
        
        # الخطوة 2: كتابة البيانات
        driver.find_element(By.NAME, "email").send_keys(user_id)
        driver.find_element(By.NAME, "pass").send_keys(password)
        send_step_screenshot(message.chat.id, driver, "2️⃣ تم إدخال الإيميل والباسورد")
        
        # الخطوة 3: الضغط على الدخول
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
        bot.send_message(message.chat.id, "🔘 تم الضغط على زر تسجيل الدخول.. انتظر النتيجة.")
        time.sleep(6)
        
        # الخطوة 4: النتيجة النهائية
        send_step_screenshot(message.chat.id, driver, f"🏁 النتيجة النهائية\n🔗 الرابط: {driver.current_url}")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:150]}")
    finally:
        driver.quit()

print("البوت يعمل بنظام تتبع الخطوات...")
bot.infinity_polling()
