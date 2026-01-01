import telebot
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def start():
    try:
        bot.send_message(CHAT_ID, "🧹 تم تنظيف المستودع.. محاولة جديدة الآن برابط mbasic.")
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36")
        
        driver = webdriver.Chrome(options=opts)
        driver.get("https://mbasic.facebook.com/")
        time.sleep(random.randint(5, 8))
        
        driver.find_element(By.NAME, "email").send_keys("61583389620613")
        driver.find_element(By.NAME, "pass").send_keys("jasser vodka")
        driver.find_element(By.NAME, "login").click()
        
        time.sleep(12)
        driver.save_screenshot("clean_start.png")
        with open("clean_start.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 نتيجة أول محاولة بعد التنظيف")
        driver.quit()
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ: {str(e)}")

if __name__ == "__main__":
    start()
