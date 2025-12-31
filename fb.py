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
    msg = bot.send_message(message.chat.id, "🚀 البوت "المجبر" جاهز.\nأرسل الـ ID:")
    bot.register_next_step_handler(msg, step1)

def step1(message):
    uid = message.text
    msg = bot.send_message(message.chat.id, "أرسل كلمة السر:")
    bot.register_next_step_handler(msg, step2, uid)

def step2(message, uid):
    pas = message.text
    bot.send_message(message.chat.id, "⌛ جاري الإجبار على النسخة المجانية ومنع التوجيه...")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # استخدام User-Agent لجهاز قديم (لأن الأجهزة القديمة تُجبر فيسبوك على البقاء في النسخة المجانية)
    opts.add_argument('user-agent=Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36')
    
    driver = webdriver.Chrome(options=opts)

    try:
        # الدخول المباشر لرابط تسجيل الدخول في النسخة المجانية
        driver.get("https://free.facebook.com/login/?next&ref=dbl&fl&refid=8")
        time.sleep(3)

        # فحص: هل قام فيسبوك بتغيير الرابط؟ إذا نعم، أعده بالقوة
        if "free.facebook.com" not in driver.current_url:
            driver.get("https://free.facebook.com/login.php")
            time.sleep(2)

        capture(message.chat.id, driver, "1️⃣ تم تثبيت الصفحة على النسخة المجانية")

        # إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        
        # محاولة الضغط على الزر مع منع التوجيه بعد الضغط
        try:
            btn = driver.find_element(By.NAME, "login")
            btn.click()
        except:
            driver.execute_script("document.forms[0].submit();") # إرسال الفورم برمجياً إذا اختفى الزر

        bot.send_message(message.chat.id, "🔘 تم إرسال البيانات.. جاري مراقبة النتيجة.")
        time.sleep(8)
        
        # التقاط النتيجة النهائية مع الرابط
        final_url = driver.current_url
        capture(message.chat.id, driver, f"🏁 النتيجة النهائية\nالرابط الحالي: {final_url}")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)[:100]}")
        capture(message.chat.id, driver, "📸 صورة للوضع الحالي")
    finally:
        driver.quit()

bot.infinity_polling()
