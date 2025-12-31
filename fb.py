import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def send_file(chat_id, driver, caption):
    try:
        path = f"step_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            bot.send_document(chat_id, f, caption=caption)
        time.sleep(1)
        if os.path.exists(path): os.remove(path)
    except: pass

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "🚀 نظام معالجة الصفحة البيضاء مفعل.\nأرسل الـ ID:")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري المحاولة.. سننتظر طويلاً لتجنب الصفحة البيضاء.")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # تغيير البصمة لجهاز أندرويد متوسط القوة لثبات الاتصال
    opts.add_argument('user-agent=Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36')
    
    driver = webdriver.Chrome(options=opts)

    try:
        driver.get("https://free.facebook.com/login.php")
        time.sleep(4)
        
        # إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        
        # الضغط
        btn = driver.find_element(By.NAME, "login")
        driver.execute_script("arguments[0].click();", btn)
        
        bot.send_message(message.chat.id, "🔘 تم الضغط.. جاري الانتظار 15 ثانية للتغلب على التعليق.")
        
        # انتظار طويل (15 ثانية) لأن السيرفر قد يكون بطيئاً في التحويل
        time.sleep(15)
        
        # فحص إذا كانت الصفحة لا تزال بيضاء (نقوم بعمل تحديث)
        if "free.facebook.com" in driver.current_url and len(driver.page_source) < 500:
            bot.send_message(message.chat.id, "⚠️ الصفحة بيضاء.. جاري عمل Refresh...")
            driver.refresh()
            time.sleep(7)

        send_file(message.chat.id, driver, f"🏁 النتيجة النهائية\nالرابط: {driver.current_url}")
        
        # إذا كان الرابط لا يزال يحتوي على login، فهذا يعني فشل الدخول
        if "login" in driver.current_url:
            bot.send_message(message.chat.id, "❌ يبدو أن البيانات خاطئة أو تم حظر المحاولة.")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:100]}")
    finally:
        driver.quit()

bot.infinity_polling()
