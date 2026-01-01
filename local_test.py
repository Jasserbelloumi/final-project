import telebot
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# إعدادات البوت والحساب
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def run_local():
    print("🚀 بدء محاكاة الدخول من Termux...")
    bot.send_message(CHAT_ID, "📱 محاولة دخول محلي (بصمة آيفون) بدأت الآن...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    # استخدام نفس بصمة الآيفون المتفق عليها
    iphone_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    opts.add_argument(f"user-agent={iphone_ua}")
    
    try:
        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(390, 844)
        
        # الانتقال لرابط mbasic
        driver.get("https://mbasic.facebook.com/")
        time.sleep(5)
        
        # إدخال البيانات
        print("📝 كتابة البيانات...")
        email_input = driver.find_element(By.NAME, "email")
        pass_input = driver.find_element(By.NAME, "pass")
        
        email_input.send_keys("61583389620613")
        pass_input.send_keys("jasser vodka")
        
        time.sleep(1)
        
        # آلية تسجيل الدخول عبر مفتاح ENTER
        print("⌨️ إرسال أمر الدخول (ENTER)...")
        pass_input.send_keys(Keys.ENTER)
        
        # الانتظار لرؤية النتيجة (تأكيد أو دخول أو كابتشا)
        time.sleep(12)
        
        # التقاط الصورة
        photo_path = "termux_snap.png"
        driver.save_screenshot(photo_path)
        
        # إرسال الصورة للتلجرام
        with open(photo_path, "rb") as photo:
            bot.send_photo(CHAT_ID, photo, caption="📸 نتيجة الدخول من Termux (بصمة آيفون)")
        
        print("✅ تم الإرسال للتلجرام بنجاح!")
        os.remove(photo_path)
        
    except Exception as e:
        error_msg = f"❌ خطأ محلي: {str(e)}"
        print(error_msg)
        bot.send_message(CHAT_ID, error_msg)
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_local()
