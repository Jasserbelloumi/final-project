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
    # إرسال رسالة تجريبية فوراً عند بدء البايثون
    print("Sending start message...")
    bot.send_message(CHAT_ID, "🚀 السكربت اشتغل الآن على سيرفرات GitHub!")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get("https://m.facebook.com/login/")
        time.sleep(5)
        
        bot.send_message(CHAT_ID, "🔎 جاري محاولة تسجيل الدخول للحساب المطلوب...")
        
        driver.find_element(By.NAME, "email").send_keys("61583389620613")
        driver.find_element(By.NAME, "pass").send_keys("jasser vodka")
        
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
            
        time.sleep(10)
        
        # تصوير النتيجة مهما كانت
        driver.save_screenshot("check.png")
        with open("check.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 هذه هي النتيجة التي ظهرت لي")
            
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ حدث خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start()
