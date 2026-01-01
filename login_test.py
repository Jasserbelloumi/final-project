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
        bot.send_message(CHAT_ID, "🔍 محاولة جديدة: البحث عن العناصر بمرونة أكبر...")
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36")
        
        driver = webdriver.Chrome(options=opts)
        driver.get("https://mbasic.facebook.com/")
        
        # انتظار تحميل حقل الإيميل للتأكد من أن الصفحة فتحت
        wait = WebDriverWait(driver, 15)
        email_field = wait.until(EC.presence_of_element_status((By.NAME, "email")))
        
        # إدخال البيانات
        driver.find_element(By.NAME, "email").send_keys("61583389620613")
        driver.find_element(By.NAME, "pass").send_keys("jasser vodka")
        
        # محاولة الضغط على الزر بأكثر من طريقة
        try:
            # الطريقة الأولى: البحث بالاسم المعتاد
            driver.find_element(By.NAME, "login").click()
        except:
            try:
                # الطريقة الثانية: البحث عبر زر الإرسال (Submit)
                driver.find_element(By.XPATH, "//input[@type='submit']").click()
            except:
                # الطريقة الثالثة: الضغط عبر Enter
                driver.find_element(By.NAME, "pass").send_keys(u'\ue007')
        
        time.sleep(12)
        driver.save_screenshot("flex_result.png")
        with open("flex_result.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 نتيجة المحاولة بعد تعديل البحث عن العناصر")
        driver.quit()
        
    except Exception as e:
        # التقاط صورة حتى في حالة الخطأ لمعرفة أين توقف البوت
        try:
            driver.save_screenshot("error_page.png")
            with open("error_page.png", "rb") as p:
                bot.send_photo(CHAT_ID, p, caption=f"❌ تعذر العثور على العنصر. هذه صورة لما يراه البوت الآن:\n\n{str(e)}")
        except:
            bot.send_message(CHAT_ID, f"❌ خطأ فادح: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    start()
