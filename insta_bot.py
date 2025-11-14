import os
import sys
import time
import random
import subprocess
from instabot import Bot

# قائمة المكتبات التي نحتاج إلى التأكد من أنها مثبتة
required_libraries = [
    "instabot"
]

# دالة لتثبيت المكتبات تلقائيًا إذا كانت مفقودة
def setup_environment():
    for library in required_libraries:
        try:
            __import__(library)
            print(f"✅ '{library}' مكتبة موجودة.")
        except ImportError:
            print(f">>> تثبيت المكتبة المطلوبة: {library}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# بيانات الدخول
USERNAME = "sjsoqoqkmbii21"
PASSWORD = "houdaelmastr3##12"
SESSION_FILE = "session.json"
AUTO_REPLY_MESSAGE = "Hello, thank you for your message. We will reply to you as soon as possible. Thank you!"

# تسجيل الدخول مع دعم الجلسات
def login():
    bot = Bot()

    # تحميل الجلسة إذا كانت موجودة
    if os.path.exists(SESSION_FILE):
        try:
            bot.load_settings(SESSION_FILE)
            bot.login(username=USERNAME, password=PASSWORD)
            print("✅ تم تسجيل الدخول باستخدام الجلسة المحفوظة.")
            return bot
        except Exception as e:
            print(f"⚠️ فشل في تحميل الجلسة، إعادة المحاولة بتسجيل دخول جديد: {e}")

    # تسجيل الدخول بشكل طبيعي
    bot.login(username=USERNAME, password=PASSWORD)
    bot.dump_settings(SESSION_FILE)
    print("✅ تسجيل الدخول بنجاح.")
    
    return bot

# جلب معلومات الحساب بشكل آمن
def get_account_info(bot):
    try:
        user_info = bot.get_user_info(bot.user_id)
        print("\n📊 معلومات الحساب:")
        print(f"👤 الاسم الكامل: {user_info['full_name']}")
        print(f"🧑‍💻 اسم المستخدم: {user_info['username']}")
        print(f"🔹 المتابعين: {user_info['follower_count']}")
        print(f"🔸 المتابعين لهم: {user_info['following_count']}")
        print(f"🔄 المنشورات: {user_info['media_count']}")
        print("===================================")
    except Exception as e:
        print(f"❌ فشل في جلب معلومات الحساب بشكل آمن: {e}")

# محاكاة الكتابة البشرية
def simulate_typing(text, delay=0.15):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(random.uniform(0.05, delay))
    print()

# الرد التلقائي على الرسائل المباشرة
def auto_reply(bot):
    print("⏳ بدأ المراقبة للرسائل المباشرة...")

    while True:
        try:
            threads = bot.get_messages()

            if not threads:
                print("💤 لا توجد رسائل جديدة.")

            for thread in threads:
                try:
                    messages = bot.get_messages(thread)

                    for msg in messages:
                        if msg['user_id'] != bot.user_id:
                            print(f"📩 رسالة واردة: {msg['text']}")
                            print("✅ الكتابة والرد التلقائي...")

                            simulate_typing(AUTO_REPLY_MESSAGE)
                            bot.send_message(AUTO_REPLY_MESSAGE, thread)
                            print("✅ تم إرسال الرد التلقائي.")
                            time.sleep(random.uniform(3, 6))

                except Exception as e:
                    print(f"❌ خطأ أثناء فحص الرسائل في الخيط {thread['id']}: {e}")
                    time.sleep(30)

            time.sleep(random.uniform(60, 120))

        except Exception as e:
            print(f"❌ خطأ عام في الحلقة: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # تأكيد تحميل جميع المكتبات المطلوبة
    setup_environment()

    # تسجيل الدخول
    bot = login()

    # جلب معلومات الحساب
    get_account_info(bot)

    # الرد التلقائي على الرسائل
    auto_reply(bot)
