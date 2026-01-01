import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def start():
    bot.send_message(CHAT_ID, "🌐 جاري تجربة تسجيل الدخول عبر رابط جديد (Instagram)...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
    
    driver = webdriver.Chrome(options=opts)
    try:
        # التغيير إلى انستجرام للتجربة
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(6) # انتظار تحميل الصفحة
        
        bot.send_message(CHAT_ID, "📝 جاري إدخال البيانات في Instagram...")
        
        # البحث عن حقول الإدخال في انستجرام
        try:
            user_input = driver.find_element(By.NAME, "username")
            pass_input = driver.find_element(By.NAME, "password")
            
            user_input.send_keys("61583389620613")
            pass_input.send_keys("jasser vodka")
            
            time.sleep(2)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(10)
        except Exception as e:
            print(f"Elements not found: {e}")

        # التقاط صورة للنتيجة
        driver.save_screenshot("insta_result.png")
        with open("insta_result.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 نتيجة محاولة دخول Instagram")
            
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start()
