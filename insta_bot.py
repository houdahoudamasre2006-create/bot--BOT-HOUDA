import time
import requests
import subprocess
import sys
import os # ⚠️ تم إضافة مكتبة os لقراءة متغيرات البيئة

# --- التثبيت التلقائي للمكتبات (يعمل قبل الاستيراد) ---
# ملاحظة: هذا الجزء قد لا يعمل في بيئات GitHub Actions الحديثة ويجب تثبيت المكتبات بشكل صريح في ملف YAML. 
# لكننا سنبقيه كما طلبته.
def install_libraries():
    """تحميل المكتبات المطلوبة (instabot و requests) إذا لم تكن مثبتة."""
    required_libraries = ['instabot', 'requests']
    print("⚙️ جاري التحقق من المكتبات المطلوبة...")
    
    # التأكد من أن مكتبة requests متاحة
    if 'requests' not in sys.modules:
        try:
             subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
             print("✅ تم تثبيت requests بنجاح.")
        except:
             pass

    for lib in required_libraries:
        try:
            # محاولة استيراد المكتبة
            __import__(lib)
            print(f"✅ تم العثور على مكتبة: {lib}")
        except ImportError:
            # إذا لم يتم العثور عليها، يتم تثبيتها
            print(f"❌ لم يتم العثور على مكتبة: {lib}. جاري التثبيت...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                print(f"✅ تم تثبيت {lib} بنجاح.")
            except Exception as e:
                print(f"❌ فشل تثبيت {lib}. يرجى محاولة التثبيت يدوياً: pip install {lib}")
                sys.exit(1) # إيقاف التشغيل إذا فشل التثبيت
            
# استدعاء دالة التثبيت أولاً
install_libraries()

# الآن يمكن استيراد المكتبات بأمان
from instabot import Bot

# --- 1. معلومات تسجيل الدخول لحساب إنستغرام (يجب تغييرها) ---
# ⚠️ تم تعديل هذا الجزء لقراءة البيانات من متغيرات البيئة (GitHub Secrets)
INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME", "xx0905443")
INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD", "rZUXNM6Q")

# --- 2. معلومات بوت تليجرام (يجب تغييرها) ---
# ⚠️ تم تعديل هذا الجزء لقراءة البيانات من متغيرات البيئة (GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8509450378:AAGAREYYDbwxYsoxhf3mMYYToSsOgQvi1_E")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "5512967645")

# نص الرد التلقائي
AUTO_REPLY_MESSAGE = "مرحباً! شكراً على رسالتك. يبدو أن المطور نائم😴 وسيتم الرد عليك في أقرب وقت. شكراً لك."
TELEGRAM_MESSAGE_PREFIX = "🚨 رسالة جديدة من إنستغرام تحتاج للرد 🚨\n\n"
TELEGRAM_MESSAGE_SUFFIX = "\n\n✅ تم الرد على المستخدم تلقائياً على إنستغرام."

def send_telegram_message(text):
    """إرسال رسالة إلى تليجرام باستخدام التوكن والمعرف"""
    # ⚠️ نستخدم المتغيرات التي تم قراءتها من البيئة
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ فشل إرسال الرسالة إلى تليجرام: {e}")

def get_user_details(bot, user_id):
    """جلب معلومات إضافية للمستخدم (المتابعين ومن يتابعهم)"""
    try:
        user_info = bot.get_user_info(user_id)
        
        if user_info and user_info.get('follower_count') is not None:
            followers = user_info['follower_count']
            following = user_info['following_count']
            full_name = user_info.get('full_name', 'N/A')
            
            return followers, following, full_name
        
    except Exception as e:
        print(f"⚠️ فشل جلب تفاصيل المستخدم الإضافية: {e}")
        
    return "N/A", "N/A", "N/A"


def get_and_reply_to_dms(bot, replied_user_ids):
    """جلب الرسائل الجديدة والرد عليها"""
    print("🔄 جاري التحقق من الرسائل المباشرة الجديدة...")
    
    try:
        inbox = bot.get_inbox_messages()
    except Exception as e:
        print(f"❌ فشل في جلب صندوق الوارد: {e}")
        return replied_user_ids, 0
    
    messages_count = 0
    
    if inbox and isinstance(inbox, list):
        for thread in inbox:
            thread_id = thread.get('thread_id')
            
            if thread_id and thread_id not in replied_user_ids:
                try:
                    latest_message = thread['items'][0]
                    user_id = thread['users'][0]['pk']
                    username = thread['users'][0]['username']
                    text = latest_message.get('text')
                    
                    if text:
                        messages_count += 1
                        
                        # جلب معلومات المستخدم الإضافية
                        followers, following, full_name = get_user_details(bot, user_id)
                        
                        # تجهيز رسالة التليجرام
                        full_message = (
                            f"{TELEGRAM_MESSAGE_PREFIX}"
                            f"*معلومات المستخدم*\n"
                            f"**اسم المستخدم (Username):** @{username}\n"
                            f"**الاسم الكامل:** {full_name}\n"
                            f"**عدد المتابعين (Followers):** {followers}\n"
                            f"**عدد من يتابعهم (Following):** {following}\n"
                            f"**عدد الرسائل في الشات (تقريبي):** {len(thread.get('items', []))}\n"
                            f"---"
                            f"\n*الرسالة التي وصلت*\n"
                            f"**الرسالة:** {text}\n"
                            f"{TELEGRAM_MESSAGE_SUFFIX}"
                        )
                        
                        # 1. إرسال الرسالة إلى تليجرام
                        send_telegram_message(full_message)
                        
                        # 2. الرد التلقائي على الرسالة في إنستغرام
                        bot.send_message(AUTO_REPLY_MESSAGE, user_id)
                        print(f"✅ تم الرد على @{username}: وتم إرسال التقرير لتليجرام.")
                        
                        replied_user_ids.add(thread_id) 

                except Exception as e:
                    print(f"❌ حدث خطأ أثناء معالجة رسالة: {e}")
                    continue
    else:
        print("ℹ️ لا يوجد صندوق وارد أو تنسيق غير متوقع.")
        
    return replied_user_ids, messages_count

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    
    # تهيئة البوت وتسجيل الدخول
    bot = Bot()
    print(f"⚙️ جاري محاولة تسجيل الدخول لحساب: {INSTAGRAM_USERNAME}...")
    try:
        # هنا قد تحتاج instabot إلى إنشاء ملفات cache (الملفات المؤقتة) في المجلد الذي يشغل منه البوت
        bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
        print("✅ تم تسجيل الدخول بنجاح!")
    except Exception as e:
        print(f"❌ فشل تسجيل الدخول: {e}")
        # ملاحظة: إذا كان الفشل بسبب Instabot، قد تحتاج إلى حذف ملفات cache المؤقتة.
        return

    replied_user_ids = set()
    total_replied_count = 0
    
    # حلقة التشغيل الرئيسية
    while True:
        try:
            replied_user_ids, current_replied_count = get_and_reply_to_dms(bot, replied_user_ids)
            total_replied_count += current_replied_count
            
            print(f"\n--- ملخص ---")
            print(f"إجمالي الرسائل التي تم الرد عليها حتى الآن: {total_replied_count}")
            print(f"الانتظار لمدة 300 ثانية (5 دقائق) قبل التحقق مجدداً...")
            print("-------------\n")
            
            time.sleep(300) 

        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف البوت يدوياً.")
            break
        except Exception as e:
            print(f"\n❌ حدث خطأ غير متوقع في الحلقة الرئيسية: {e}")
            time.sleep(600) 

    bot.logout()
    print("👋 تم تسجيل الخروج من إنستغرام.")

if __name__ == "__main__":
    main()
