import telebot
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def start():
    try:
        bot.send_message(CHAT_ID, "🚀 محاولة النقر القوية (Force Click) بدأت...")
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36")
        
        driver = webdriver.Chrome(options=opts)
        driver.get("https://mbasic.facebook.com/")
        
        wait = WebDriverWait(driver, 20)
        
        # إدخال البيانات
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys("61583389620613")
        
        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.send_keys("jasser vodka")
        
        bot.send_message(CHAT_ID, "⌨️ جاري محاولة الدخول عبر إرسال أمر Enter البرمجي...")
        
        # الطريقة 1: إرسال مفتاح Enter مباشرة (أضمن طريقة لتجاوز الأزرار المخفية)
        pass_field.send_keys(Keys.ENTER)
        
        time.sleep(5)
        
        # الطريقة 2 (احتياطية): النقر باستخدام JavaScript على أي زر يحتوي نص 'Log In'
        driver.execute_script("""
            var buttons = document.querySelectorAll('button, input, a');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].innerText.includes('Log In') || buttons[i].value.includes('Log In') || buttons[i].name === 'login') {
                    buttons[i].click();
                    break;
                }
            }
        """)
        
        time.sleep(15)
        
        # التقاط النتيجة
        driver.save_screenshot("force_click.png")
        with open("force_click.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 النتيجة بعد محاولة النقر الإجباري وإرسال Enter")
            
        driver.quit()
        
    except Exception as e:
        try:
            driver.save_screenshot("fail.png")
            with open("fail.png", "rb") as p:
                bot.send_photo(CHAT_ID, p, caption=f"❌ لا يزال هناك مشكلة:\n{str(e)}")
        except:
            bot.send_message(CHAT_ID, f"❌ خطأ فادح: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    start()
