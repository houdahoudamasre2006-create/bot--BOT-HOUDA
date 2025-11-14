import os

import sys

import time

import random

import json

import subprocess

from instagrapi import Client

from instagrapi.exceptions import LoginRequired, BadCredentials, TwoFactorRequired



USERNAME = "sjsoqoqkmbii21"

PASSWORD = "houdaelmastr3##12"

SESSION_FILE = "session.json"

AUTO_REPLY_MESSAGE = "Hello, thank you for your message. We will reply to you as soon as possible. Thank you!"



# Check if required libraries are installed

def setup_environment():

    try:

        __import__("instagrapi")

        print("✅ 'instagrapi' library found.")

    except ImportError:

        print(">>> Installing required library: instagrapi")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "instagrapi"])



# Login with session support

def login():

    cl = Client()



    if os.path.exists(SESSION_FILE):

        try:

            cl.load_settings(SESSION_FILE)

            cl.login(USERNAME, PASSWORD)

            print("✅ Logged in using saved session.")

            return cl

        except Exception as e:

            print(f"⚠️ Failed to load session, retrying fresh login: {e}")



    try:

        cl.login(USERNAME, PASSWORD)

        cl.dump_settings(SESSION_FILE)

        print("✅ Login successful.")

    except TwoFactorRequired:

        code = input("Enter 2FA code: ")

        cl.login(USERNAME, PASSWORD, verification_code=code)

        cl.dump_settings(SESSION_FILE)

        print("✅ Login successful with 2FA.")

    except BadCredentials as e:

        print(f"❌ Invalid username or password: {e}")

        sys.exit(1)

    except Exception as e:

        print(f"❌ Unexpected login error: {e}")

        sys.exit(1)



    return cl



# Fetch public account info safely

def get_account_info(cl):

    try:

        user_id = cl.user_id

        try:

            info = cl.user_info(user_id)

        except Exception:

            info = cl.user_info_by_username(USERNAME)



        print("\n📊 Account Info:")

        print(f"👤 Full Name: {info.full_name}")

        print(f"🧑‍💻 Username: {info.username}")

        print(f"🔹 Followers: {info.follower_count}")

        print(f"🔸 Following: {info.following_count}")

        print(f"🔄 Posts: {info.media_count}")

        print("===================================")

    except Exception as e:

        print(f"❌ Failed to fetch account info safely: {e}")



# Simulate human typing

def simulate_typing(text, delay=0.15):

    for char in text:

        print(char, end="", flush=True)

        time.sleep(random.uniform(0.05, delay))

    print()



# Auto reply to DMs

def auto_reply(cl):

    print("⏳ Starting to monitor direct messages...")



    while True:

        try:

            threads = cl.direct_threads()

            if not threads:

                print("💤 No new messages.")



            for thread in threads:

                try:

                    messages = cl.direct_messages(thread.id)

                    for msg in messages:

                        if msg.user_id != cl.user_id:

                            print(f"📩 Incoming message: {msg.text}")

                            print("✅ Typing automatic reply...")

                            simulate_typing(AUTO_REPLY_MESSAGE)

                            cl.direct_send(AUTO_REPLY_MESSAGE, thread.id)

                            print("✅ Automatic reply sent.")

                            time.sleep(random.uniform(3, 6))

                except Exception as e:

                    if "403" in str(e):

                        print(f"⚠️ Rate limit / block detected, waiting 2 minutes...")

                        time.sleep(11)

                    else:

                        print(f"❌ Error while checking thread {thread.id}: {e}")

                        time.sleep(30)



            time.sleep(random.uniform(60, 120))

        except LoginRequired:

            print("⚠️ Logged out, relogging...")

            cl = login()

        except Exception as e:

            print(f"❌ General error in loop: {e}")

            time.sleep(60)



if __name__ == "__main__":

    setup_environment()

    cl = login()

    get_account_info(cl)

    auto_reply(cl)

