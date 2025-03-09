import random
import requests
import os
import io
from datetime import datetime, time
from apscheduler.triggers.cron import CronTrigger
from loader import bot
from aiogram.types import ParseMode
from aiogram import types


# Avtomatik xabar yuboruvchi funksiya
async def send_message_user(telegram_id, message, fan1, fan2):
    try:
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
            "Geografiya": 10,
            "Huquq": 12
        }

        fan1_id = fanlar_json[fan1]
        fan2_id = fanlar_json[fan2]
        user_id = random.randint(2, 70)

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
                await bot.send_message(chat_id=telegram_id, text="🔑 Test javoblarini yuborish boʻyicha qoʻllanma bilan tanishib chiqing!\n\n📹 Vidoe qoʻllanma: 👉 https://youtu.be/0Z_AEHM1AWc")

                user_status_updt = os.getenv('BLOK_TEST_PATCH')
                r = requests.patch(f"{user_status_updt}{telegram_id}", data={'status': 'yechmoqda'})
                if r.status_code == 200:
                    await bot.send_message(chat_id=5605407368,
                                           text=f"✅ Muvaffaqiyatli test materiallari yuborildi va foydalanuvchi testlarni yechmoqda\n\nChat id: {telegram_id}\nStatus kod: {r.status_code}")
                else:
                    await bot.send_message(chat_id=5605407368,
                                           text=f"⚠️ STATUS O'ZGARMADI\n\nChat id: {telegram_id}\nStatus kod: {r.status_code}")

            else:
                await bot.send_message(chat_id=telegram_id, text="Qandaydir xatolik bo'ldi... 🤷‍♂️")
                await bot.send_message(chat_id=5605407368,
                                       text=f"⚠️ Fayl yuborilmadi\n\nChat id: {telegram_id}\nStatus kod: {req_file.status_code}")
        else:
            print('test yuklash status: ', req.status_code)
            await bot.send_message(chat_id=telegram_id,
                                   text="Test yuklashda nimadur xato ketdi, xatolikni bartaraf etish uchun adminga xabar yuborildi!")
            await bot.send_message(chat_id=5605407368, text=f"Test yuborilmadi...\n\n{get_data}\nStatus kod: {req.status_code}")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")


# API ma'lumotlarini olish va xabarlarni rejalashtirish
async def schedule_notifications(scheduler):
    try:
        response = requests.get(os.getenv('BLOK_TEST_ALL'))
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
                    args=[telegram_id, message, blok1, blok2],
                    misfire_grace_time=300
                )

    except requests.exceptions.RequestException as e:
        print(f"API bilan bog'liq xatolik: {e}")


# Har yakshanba va belgilangan vaqtlarda rejalashtirish
def setup_scheduled_notifications(scheduler):
    for hour in [8, 10, 14, 18, 20]:
        scheduler.add_job(
            schedule_notifications, 
            CronTrigger(hour=hour, minute=0),
            args=[scheduler]
        )


# #                           ### Test uchun sinov ###
# def setup_scheduled_notifications(scheduler):
#     # Haftaning chorshanba kuni uchun trigger
#     trigger = CronTrigger(day_of_week='thu', hour=12, minute=0)  # Har chorshanba 12:00 PM
#     scheduler.add_job(schedule_notifications, trigger, args=[scheduler])
#
#     # PM vaqtlari uchun: 12:00, 14:00, 16:00, 18:00, 20:00
#     for minut in [37, 21, 27, 18, 56]:
#         scheduler.add_job(schedule_notifications, CronTrigger(day_of_week='thu', hour=19, minute=minut), args=[scheduler])
