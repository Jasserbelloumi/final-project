import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def start():
    try:
        bot.send_message(CHAT_ID, "🍏 محاولة دخول نهائية من GitHub ببصمة آيفون...")
        
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        # بصمة آيفون 15 برو ماكس
        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        opts.add_argument(f"user-agent={ua}")
        
        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(390, 844)
        
        driver.get("https://mbasic.facebook.com/")
        time.sleep(7)
        
        # إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys("61583389620613")
        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.send_keys("jasser vodka")
        
        # الضغط على Enter (أضمن طريقة)
        pass_field.send_keys(Keys.ENTER)
        
        # محاولة نقر إضافية بـ JS للضمان
        driver.execute_script("document.querySelector('input[type=\"submit\"], input[name=\"login\"]').click();")
        
        time.sleep(15)
        
        # تصوير النتيجة
        driver.save_screenshot("github_result.png")
        with open("github_result.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 النتيجة من سيرفرات GitHub")
        
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ حدث خطأ في GitHub: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start()
