import telebot
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def send_file(chat_id, driver, caption):
    try:
        path = f"file_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            bot.send_document(chat_id, f, caption=caption)
        time.sleep(1)
        if os.path.exists(path): os.remove(path)
    except: pass

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "🚀 نظام الإجبار على FreeFB مفعل.\nأرسل الـ ID:")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري إجبار فيسبوك وتخطي الحواجز...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # تمويه المتصفح كأنه هاتف قديم جداً (هذا يضمن بقاء النسخة المجانية)
    opts.add_argument('user-agent=Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; GT-S5830i Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
    
    driver = webdriver.Chrome(options=opts)

    try:
        # 1. الدخول والإجبار على الرابط
        driver.get("https://free.facebook.com/login.php")
        time.sleep(3)
        
        # كود جافا سكريبت لحذف أي "طبقة" تمنع الضغط (Overlay Remover)
        driver.execute_script("""
            var overlays = document.querySelectorAll('div[style*="fixed"], div[style*="absolute"]');
            for (var i = 0; i < overlays.length; i++) {
                if (overlays[i].innerText.includes('بلدك') || overlays[i].innerText.length < 5) {
                    overlays[i].remove();
                }
            }
        """)
        
        send_file(message.chat.id, driver, "1- محاولة فتح Free FB")

        # 2. إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        send_file(message.chat.id, driver, "2- إدخال البيانات")

        # 3. الضغط الخارق (تخطي الطبقات بالنقرة المباشرة على العنصر)
        bot.send_message(message.chat.id, "🔘 جاري تجاوز الحماية والضغط...")
        
        # محاولة الضغط عبر محاكاة نقرة حقيقية تتجاهل العوائق
        try:
            btn = driver.find_element(By.NAME, "login")
            driver.execute_script("arguments[0].click();", btn)
        except:
            driver.execute_script("document.querySelector('input[type=\"submit\"], button[type=\"submit\"]').click();")
        
        # 4. تصوير النتيجة الفورية
        time.sleep(2)
        send_file(message.chat.id, driver, "3- لقطة بعد الضغط مباشرة")
        
        # 5. انتظار النتيجة النهائية
        time.sleep(7)
        bot.send_message(message.chat.id, f"🏁 الرابط الحالي: {driver.current_url}")
        send_file(message.chat.id, driver, "4- النتيجة النهائية")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:100]}")
    finally:
        driver.quit()

bot.infinity_polling()
