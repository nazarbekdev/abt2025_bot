import os
import requests
from aiogram.types import Message
from loader import dp, bot
from keyboards.inline.dostlarni_taklif_qilish import taklif_qilish
from dotenv import load_dotenv

load_dotenv()


@dp.message_handler(lambda message: message.text == "💰 Balans")
async def balans(message: Message):
    referal_link = f"https://t.me/abt2025_bot?start={message.from_user.id}"
    url = os.getenv('USER_INFO')
    user_data = requests.get(f"{url}{message.from_user.id}").json()
    balans = user_data['balans']
    karta_raqam = os.getenv("CARD_NUMBER")
    await message.answer(f"Siznig hisobingiz: {balans} so'm\n\n"
                         f"👇 Hisobingizni to'ldirish uchun 👇\n"
                         f"💳 {karta_raqam}\n"
                         f"Nazarbek Qobulov\n\n"
                         f"To'lov chekini(screenshot) @abt2025_admin ga yuboring!\n"
                         f"Balansingiz qisqa vaqt ichida to'ldiriladi!", reply_markup=taklif_qilish(referal_link))
