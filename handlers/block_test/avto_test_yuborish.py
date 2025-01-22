import random

import requests
import os
import io
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loader import bot
from aiogram.types import ParseMode
from aiogram import types

# API URL
API_URL = "http://127.0.0.1:8000/api/v1/block-test-all"

# Scheduler
scheduler = AsyncIOScheduler()


# Avtomatik xabar yuboruvchi funksiya
async def send_message_user(telegram_id, message, fan1, fan2):
    try:
        print('Fan1:', fan1)
        print('Fan2:', fan2)
        if fan1 == "Huquq" or fan2 == "Huquq":
            baza = 2
        else:
            baza = 1
        fanlar_json = {
            "Matematika": 7,
            "Fizika": 6,
            "Biologiya": 4,
            "Kimyo": 8,
            "Ona tili va adabiyot": 9,
            "Ingliz tili": 11,
            "Tarix": 5,
            "Geografia": 10,
            "Huquq": 12
        }

        fan1_id = fanlar_json[fan1]
        fan2_id = fanlar_json[fan2]
        user_id = random.randint(2, 70)
        print('Fan1 ID:', fan1_id)
        print('Fan2 ID:', fan2_id)
        print('User ID:', user_id)
        get_data = {
            "number_books": 1,
            "database_type": baza,
            "subject1": fan1_id,
            "subject2": fan2_id,
            "language": 1,
            "user": user_id
        }

        url = os.getenv("TEST_BUYURTMA_POST")
        req = requests.post(url, data=get_data)
        if req.status_code == 200:
            await bot.send_message(chat_id=telegram_id, text=message, parse_mode=ParseMode.HTML)

            url_file = os.getenv("TEST_DOWNLOAD_GET_ID")
            req_file = requests.get(f"{url_file}{user_id}")

            if req_file.status_code == 200:
                file_content = req_file.content
                file_name = f"BlokTest.pdf"

                # Faylni yuborish
                await bot.send_document(
                    chat_id=telegram_id,
                    document=types.InputFile(io.BytesIO(file_content), filename=file_name),
                    caption="❗️Diqqat. Rejalashtirilgan vaqt ichida javoblarni yuboring!\n\n© 2024 TestifyHub")
                user_status_updt = os.getenv('BLOK_TEST_PATCH')
                r = requests.patch(f"{user_status_updt}{telegram_id}", data={'status': 'yechmoqda'})
                print('patch status:', r.status_code)
                print(r.json())
            else:
                await bot.send_message(chat_id=telegram_id, text="Qandaydir xatolik bo'ldi... 🤷‍♂️")
        else:
            print('test yuklash status: ', req.status_code)
            await bot.send_message(chat_id=telegram_id, text="Test yuklashda nimadur xato ketdi, xatolikni bartaraf etish uchun adminga xabar yuborildi!")
            await bot.send_message(chat_id=5605407368, text=f"Test yuborilmadi...\n\n{get_data}")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")


# API ma'lumotlarini olish va xabarlarni rejalashtirish
async def schedule_notifications():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        today_date = datetime.now().strftime("%d.%m.%y")
        for item in data:
            # Bugungi sanani tekshirish
            if today_date in item["rejalashtirilgan_vaqt"]:
                # Xabarni olish
                telegram_id = item["telegram_id"]
                start_time = item["rejalashtirilgan_vaqt"].split('⏰')[1].strip().split(' - ')[0]
                blok1 = item['fan1']
                blok2 = item['fan2']
                message = (
                    f"👤 <b>{item['ism_familiya']}</b>\n"
                    f"📞 {item['telefon_raqam']}\n"
                    f"📍 {item['viloyat']}\n"
                    f"📚 Fanlar: {blok1} va {blok2}\n"
                    f"⏰ Test vaqti: {item['rejalashtirilgan_vaqt']}\n"
                    "✅ Sizga omad tilaymiz!"
                )

                # Sana va vaqtni to'liq formatlash
                current_date = datetime.now().strftime("%Y-%m-%d")
                full_datetime = datetime.strptime(f"{current_date} {start_time}", "%Y-%m-%d %H:%M")

                # Foydalanuvchiga xabarni rejalashtirish
                scheduler.add_job(
                    send_message_user,
                    'date',
                    run_date=full_datetime,
                    args=[telegram_id, message, blok1, blok2]
                )

    except requests.exceptions.RequestException as e:
        print(f"API bilan bog'liq xatolik: {e}")


# # Har yakshanba va belgilangan vaqtlarda rejalashtirish
# def setup_scheduled_notifications():
#     trigger = CronTrigger(day_of_week='sun', hour=8, minute=0)
#     scheduler.add_job(schedule_notifications, trigger)
#
#     for hour in [8, 10, 14, 18, 20]:
#         scheduler.add_job(schedule_notifications, CronTrigger(day_of_week='sun', hour=hour, minute=0))


#                           ### Test uchun sinov ###
def setup_scheduled_notifications():
    # Haftaning chorshanba kuni uchun trigger
    trigger = CronTrigger(day_of_week='wed', hour=12, minute=0)  # Har chorshanba 12:00 PM
    scheduler.add_job(schedule_notifications, trigger)

    # PM vaqtlari uchun: 12:00, 14:00, 16:00, 18:00, 20:00
    for minut in [37, 25, 26, 18, 20]:
        scheduler.add_job(schedule_notifications, CronTrigger(day_of_week='wed', hour=17, minute=minut))
