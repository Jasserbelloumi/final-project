import telebot
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
bot = telebot.TeleBot(TOKEN)

def start():
    try:
        bot.send_message(CHAT_ID, "🎯 محاولة النقر المتقدمة (Fixed JS Click)...")
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36")
        
        driver = webdriver.Chrome(options=opts)
        driver.get("https://mbasic.facebook.com/")
        
        wait = WebDriverWait(driver, 20)
        
        # إدخال البيانات
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys("61583389620613")
        
        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.send_keys("jasser vodka")
        
        bot.send_message(CHAT_ID, "🖱️ جاري البحث عن الزر والنقر عليه...")

        # محاولة النقر بـ JavaScript مُحسّن (يصلح خطأ undefined)
        driver.execute_script("""
            var elements = document.querySelectorAll('input[type="submit"], input[name="login"], button[name="login"]');
            if (elements.length > 0) {
                elements[0].click();
            } else {
                // بحث شامل عن أي شيء مكتوب عليه دخول
                var all = document.querySelectorAll('input, button, a');
                for (var i = 0; i < all.length; i++) {
                    var text = all[i].innerText || all[i].value || "";
                    if (text.toLowerCase().includes('log') || text.includes('تسجيل')) {
                        all[i].click();
                        break;
                    }
                }
            }
        """)
        
        # إذا لم ينجح الـ JS، نضغط Enter كحل أخير
        time.sleep(2)
        pass_field.send_keys(Keys.ENTER)
        
        time.sleep(15)
        
        # تصوير النتيجة
        driver.save_screenshot("final_attempt.png")
        with open("final_attempt.png", "rb") as p:
            bot.send_photo(CHAT_ID, p, caption="📸 النتيجة بعد إصلاح كود النقر")
            
        driver.quit()
        
    except Exception as e:
        try:
            driver.save_screenshot("fail.png")
            with open("fail.png", "rb") as p:
                bot.send_photo(CHAT_ID, p, caption=f"❌ خطأ جديد:\n{str(e)}")
        except:
            bot.send_message(CHAT_ID, f"❌ خطأ فادح: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    start()
