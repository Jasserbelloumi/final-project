import telebot
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
bot = telebot.TeleBot(TOKEN)

def capture(chat_id, driver, text):
    path = f"step_{int(time.time())}.png"
    driver.save_screenshot(path)
    with open(path, "rb") as f:
        bot.send_photo(chat_id, f, caption=text)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "🚀 البوت المتخفي جاهز.\nأرسل الـ ID (الإيميل):")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "تمام، أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري التشغيل بنمط التخفي (Stealth Mode)...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    # --- إعدادات التخفي (التمويه) ---
    # 1. إضافة User-Agent لمتصفح كروم على أندرويد حقيقي
    user_agent = "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    opts.add_argument(f'user-agent={user_agent}')
    
    # 2. إخفاء خاصية "webdriver" التي تكتشفها المواقع
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=opts)
    
    # 3. تعديل خصائص الجافا سكريبت لتبدو كمتصفح طبيعي
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    try:
        driver.get("https://free.facebook.com/login.php")
        time.sleep(random.uniform(2, 4)) # انتظار عشوائي لتبدو كإنسان
        capture(message.chat.id, driver, "1️⃣ الصفحة الرئيسية (نمط التخفي)")

        # إدخال البيانات ببطء بسيط
        email_el = driver.find_element(By.NAME, "email")
        for char in uid:
            email_el.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3)) # محاكاة الكتابة اليدوية

        pass_el = driver.find_element(By.NAME, "pass")
        for char in pas:
            pass_el.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        capture(message.chat.id, driver, "2️⃣ تم إدخال البيانات")

        try:
            driver.find_element(By.NAME, "login").click()
        except:
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
        
        time.sleep(random.uniform(5, 8))
        capture(message.chat.id, driver, f"🏁 النتيجة النهائية\nالرابط: {driver.current_url}")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:100]}")
    finally:
        driver.quit()

bot.infinity_polling()
