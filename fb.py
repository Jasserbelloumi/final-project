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
        path = f"ios_step_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            bot.send_document(chat_id, f, caption=caption)
        time.sleep(1)
        if os.path.exists(path): os.remove(path)
    except: pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🍎 تم تفعيل نمط iPhone 14 Pro - Chrome.\nجاري محاولة الدخول للحساب المذكور...")
    # تنفيذ العملية تلقائياً للحساب الذي زودتني به
    process_login(message, "61583389620613", "jasser vodka")

def process_login(message, uid, pas):
    bot.send_message(message.chat.id, "⌛ جاري محاكاة بصمة الجهاز وتخطي الأنظمة...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    # --- بصمة آيفون 14 برو ماكس (متصفح كروم) ---
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.99 Mobile/15E148 Safari/604.1"
    opts.add_argument(f'user-agent={user_agent}')
    
    # إخفاء ملامح الأتمتة
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=opts)
    
    # إيهام المواقع أنك لست "درایفر"
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get("https://m.facebook.com/login/")
        time.sleep(random.uniform(3, 5))
        send_file(message.chat.id, driver, "🍎 واجهة الآيفون - صفحة الدخول")

        # إدخال البيانات بمحاكاة الكتابة البشرية
        email_input = driver.find_element(By.NAME, "email")
        for char in uid:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))

        pass_input = driver.find_element(By.NAME, "pass")
        for char in pas:
            pass_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))

        send_file(message.chat.id, driver, "📝 بعد كتابة البيانات (نمط آيفون)")

        # نظام البحث المرن عن زر الدخول لتجنب خطأ No such element
        bot.send_message(message.chat.id, "🔘 محاولة النقر الذكي...")
        try:
            # محاولة بالاسم
            login_btn = driver.find_element(By.NAME, "login")
            driver.execute_script("arguments[0].click();", login_btn)
        except:
            # محاولة عبر XPATH شامل لأي زر تسجيل دخول
            driver.execute_script("document.querySelector('button[type=\"submit\"], input[type=\"submit\"]').click();")
        
        time.sleep(12) # انتظار كافٍ للتحميل
        
        final_url = driver.current_url
        bot.send_message(message.chat.id, f"🏁 النتيجة النهائية:\n🔗 {final_url}")
        send_file(message.chat.id, driver, "📊 لقطة الشاشة النهائية")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:100]}")
        send_file(message.chat.id, driver, "📸 لقطة لحظة الخطأ")
    finally:
        driver.quit()

bot.infinity_polling()
