import os
import sys
import time
import random
import json
import subprocess
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, BadCredentials, TwoFactorRequired

# قائمة المكتبات التي نحتاج إلى التأكد من أنها مثبتة
required_libraries = [
    "instagrapi"
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
    cl = Client()

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            print("✅ تم تسجيل الدخول باستخدام الجلسة المحفوظة.")
            return cl
        except Exception as e:
            print(f"⚠️ فشل في تحميل الجلسة، إعادة المحاولة بتسجيل دخول جديد: {e}")

    try:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ تسجيل الدخول بنجاح.")
    except TwoFactorRequired:
        code = input("أدخل رمز 2FA: ")
        cl.login(USERNAME, PASSWORD, verification_code=code)
        cl.dump_settings(SESSION_FILE)
        print("✅ تسجيل الدخول بنجاح باستخدام 2FA.")
    except BadCredentials as e:
        print(f"❌ اسم المستخدم أو كلمة المرور غير صحيحة: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ غير متوقع أثناء تسجيل الدخول: {e}")
        sys.exit(1)

    return cl

# جلب معلومات الحساب بشكل آمن
def get_account_info(cl):
    try:
        user_id = cl.user_id
        try:
            info = cl.user_info(user_id)
        except Exception:
            info = cl.user_info_by_username(USERNAME)

        print("\n📊 معلومات الحساب:")
        print(f"👤 الاسم الكامل: {info.full_name}")
        print(f"🧑‍💻 اسم المستخدم: {info.username}")
        print(f"🔹 المتابعين: {info.follower_count}")
        print(f"🔸 المتابعين لهم: {info.following_count}")
        print(f"🔄 المنشورات: {info.media_count}")
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
def auto_reply(cl):
    print("⏳ بدأ المراقبة للرسائل المباشرة...")

    while True:
        try:
            threads = cl.direct_threads()

            if not threads:
                print("💤 لا توجد رسائل جديدة.")

            for thread in threads:
                try:
                    messages = cl.direct_messages(thread.id)

                    for msg in messages:
                        if msg.user_id != cl.user_id:
                            print(f"📩 رسالة واردة: {msg.text}")
                            print("✅ الكتابة والرد التلقائي...")

                            simulate_typing(AUTO_REPLY_MESSAGE)
                            cl.direct_send(AUTO_REPLY_MESSAGE, thread.id)
                            print("✅ تم إرسال الرد التلقائي.")
                            time.sleep(random.uniform(3, 6))

                except Exception as e:
                    if "403" in str(e):
                        print(f"⚠️ تم الوصول إلى حد المعدل أو تم الحظر، الانتظار لمدة دقيقتين...")
                        time.sleep(120)
                    else:
                        print(f"❌ خطأ أثناء فحص الرسائل في الخيط {thread.id}: {e}")
                        time.sleep(30)

            time.sleep(random.uniform(60, 120))

        except LoginRequired:
            print("⚠️ تم تسجيل الخروج، إعادة تسجيل الدخول...")
            cl = login()
        except Exception as e:
            print(f"❌ خطأ عام في الحلقة: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # تأكيد تحميل جميع المكتبات المطلوبة
    setup_environment()

    # تسجيل الدخول
    cl = login()

    # جلب معلومات الحساب
    get_account_info(cl)

    # الرد التلقائي على الرسائل
    auto_reply(cl)
