# from datetime import datetime
# import requests
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from loader import dp, bot
# from aiogram.types import ParseMode
#
# # API URL
# API_URL = "http://127.0.0.1:8000/api/v1/block-test-all"
#
# # Scheduler
# scheduler = AsyncIOScheduler()
#
#
# # Avtomatik xabar yuboruvchi funksiya
# async def send_message_user(telegram_id, message):
#     try:
#         await bot.send_message(chat_id=telegram_id, text=message)
#     except Exception as e:
#         print(f"Xatolik yuz berdi: {e}")
#
#
# # API ma'lumotlarini olish va xabarlarni rejalashtirish
# def schedule_notifications():
#     try:
#         response = requests.get(API_URL)
#         response.raise_for_status()
#         data = response.json()
#
#         today_date = datetime.now().strftime("%d.%m.%y")
#         for item in data:
#             # Bugungi sanani tekshirish
#             if today_date in item["rejalashtirilgan_vaqt"]:
#                 # Xabarni olish
#                 telegram_id = item["telegram_id"]
#                 start_time = item["rejalashtirilgan_vaqt"].split('⏰')[1].strip().split(' - ')[0]
#                 message = (
#                     f"👤 <b>{item['ism_familiya']}</b>\n"
#                     f"📞 {item['telefon_raqam']}\n"
#                     f"📍 {item['viloyat']}\n"
#                     f"📚 Fanlar: {item['fan1']} va {item['fan2']}\n"
#                     f"⏰ Test vaqti: {item['rejalashtirilgan_vaqt']}\n"
#                     "✅ Sizga omad tilaymiz!"
#                 )
#
#                 # Sana va vaqtni to'liq formatlash
#                 current_date = datetime.now().strftime("%Y-%m-%d")
#                 full_datetime = datetime.strptime(f"{current_date} {start_time}", "%Y-%m-%d %H:%M")
#
#                 # Xabarni rejalashtirish
#                 scheduler.add_job(send_message_user, 'date', run_date=full_datetime, args=[telegram_id, message])
#
#     except requests.exceptions.RequestException as e:
#         print(f"API bilan bog'liq xatolik: {e}")
#
#
# # Botni ishga tushirish va schedulerni boshlash
# async def on_startup(dispatcher):
#     # Xabarlarni rejalashtirish
#     schedule_notifications()
#     # Schedulerni boshlash
#     scheduler.start()
#
#
# if __name__ == "__main__":
#     from aiogram import executor
#
#     executor.start_polling(dp, on_startup=on_startup)

