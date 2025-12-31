import telebot
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def capture(chat_id, driver, text):
    """وظيفة التقاط وإرسال الصورة فوراً"""
    path = f"step_{int(time.time())}.png"
    driver.save_screenshot(path)
    with open(path, "rb") as f:
        bot.send_photo(chat_id, f, caption=text)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "🚀 البوت جاهز يا جاسر.\nأرسل الـ ID (الإيميل):")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "تمام، أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري بدء العملية وتتبع الخطوات بالصور...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opts)

    try:
        # خطوة 1: فتح الموقع
        driver.get("https://free.facebook.com/login.php")
        time.sleep(2)
        capture(message.chat.id, driver, "1️⃣ الصفحة الرئيسية")

        # خطوة 2: إدخال البيانات (استخدام أسماء بسيطة لتجنب الانهيار)
        driver.find_element(By.NAME, "email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        capture(message.chat.id, driver, "2️⃣ بعد كتابة البيانات")

        # خطوة 3: الضغط على الدخول
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
        
        bot.send_message(message.chat.id, "🔘 تم الضغط على زر الدخول.. ننتظر التحميل.")
        time.sleep(6)

        # خطوة 4: النتيجة النهائية
        capture(message.chat.id, driver, f"🏁 النتيجة النهائية\nالرابط: {driver.current_url}")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ تقني: {str(e)[:100]}")
    finally:
        driver.quit()

bot.infinity_polling()
