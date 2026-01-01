import telebot
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def start():
    try:
        bot.send_message(CHAT_ID, "⚙️ جاري محاولة إدخال البيانات بالكود المصحح...")
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36")
        
        driver = webdriver.Chrome(options=opts)
        driver.get("https://mbasic.facebook.com/")
        
        # استخدام الدالة الصحيحة للانتظار: presence_of_element_located
        wait = WebDriverWait(driver, 20)
        
        # البحث عن حقل الإيميل وإدخال البيانات مباشرة
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys("61583389620613")
        
        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.send_keys("jasser vodka")
        
        bot.send_message(CHAT_ID, "📝 تم إدخال البيانات بنجاح، جاري الضغط على زر الدخول...")
        
        # الضغط على زر الدخول
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            # محاولة بديلة في حال اختلف اسم الزر
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
        
        time.sleep(15)
        
        # تصوير النتيجة بعد الدخول
        driver.save_screenshot("final_step.png")
        with open("final_step.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 هذه هي النتيجة بعد محاولة تسجيل الدخول")
            
        driver.quit()
        
    except Exception as e:
        # تصوير الشاشة حتى لو فشل لمعرفة أين توقف
        try:
            driver.save_screenshot("error_fix.png")
            with open("error_fix.png", "rb") as p:
                bot.send_photo(CHAT_ID, p, caption=f"❌ خطأ أثناء العملية:\n{str(e)}")
        except:
            bot.send_message(CHAT_ID, f"❌ خطأ فادح: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    start()
