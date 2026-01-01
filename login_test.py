import telebot
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# الإعدادات
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def login_check():
    bot.send_message(CHAT_ID, "🚀 السكربت بدأ المحاولة الآن على حسابك...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
    
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get("https://m.facebook.com/login/")
        time.sleep(5)
        
        # كتابة البيانات
        driver.find_element(By.NAME, "email").send_keys("61583389620613")
        driver.find_element(By.NAME, "pass").send_keys("jasser vodka")
        
        bot.send_message(CHAT_ID, "📝 تم إدخال البيانات.. جاري الضغط على زر الدخول.")
        
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
            
        time.sleep(10)
        
        # التقاط صورة للشاشة لمعرفة ماذا حدث
        driver.save_screenshot("result.png")
        with open("result.png", "rb") as photo:
            bot.send_photo(CHAT_ID, photo, caption="📸 صورة للحالة الحالية بعد محاولة الدخول")
        
        # فحص الكوكيز
        cookies = driver.get_cookies()
        if any(c['name'] == 'c_user' for c in cookies):
            bot.send_message(CHAT_ID, "✅ مبروك! دخل الحساب بنجاح وسحبت الكوكيز.")
            with open("cookies.json", "w") as f:
                json.dump(cookies, f)
            with open("cookies.json", "rb") as f:
                bot.send_document(CHAT_ID, f)
        else:
            bot.send_message(CHAT_ID, "❌ لم يتم الدخول مباشرة.. شوف الصورة (ممكن طلب كود أو كلمة سر غلط).")
            
    except Exception as e:
        bot.send_message(CHAT_ID, f"⚠️ حدث خطأ تقني: {str(e)}")
    finally:
        driver.quit()
        if os.path.exists("result.png"): os.remove("result.png")

if __name__ == "__main__":
    login_check()
