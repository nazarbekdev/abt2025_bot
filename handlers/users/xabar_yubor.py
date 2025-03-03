import aiohttp
import asyncio
import os
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from loader import dp, bot

load_dotenv()

API_URL = os.getenv("BOT_USER_ALL")
ADMIN_ID = int(os.getenv('ADMINS'))


# **1️⃣ State yaratamiz**
class BroadcastState(StatesGroup):
    waiting_for_message = State()


@dp.message_handler(Command("xabar"))
async def ask_for_message(message: types.Message):
    """Admin /xabar komandasi yuborsa, post yozish so‘raladi"""
    if int(message.from_user.id) == ADMIN_ID:
        await message.answer("✍️ Xabar matnini yuboring.")
        await BroadcastState.waiting_for_message.set()  # **State boshlanadi**
    else:
        await message.answer("❌ Siz bu komandaning ishlashiga ruxsatga ega emassiz.")


@dp.message_handler(state=BroadcastState.waiting_for_message)
async def forward_message(message: types.Message, state: FSMContext):
    """Admin matn yuborganda barcha foydalanuvchilarga jo‘natish"""
    if message.from_user.id == ADMIN_ID:
        await message.answer("📤 Xabar yuborilmoqda...")

        # API orqali foydalanuvchilarni olish
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    users = await response.json()

                    # Har bir foydalanuvchiga xabar yuborish
                    for user in users:
                        telegram_id = user.get("telegram_id")
                        if telegram_id:
                            try:
                                await bot.send_message(telegram_id, message.text, parse_mode="HTML")
                                await asyncio.sleep(0.3)  # Antiflood uchun
                            except Exception as e:
                                logging.error(f"Xatolik {telegram_id}: {e}")

                    await message.answer("✅ Xabar barcha foydalanuvchilarga yuborildi.")
                else:
                    await message.answer("❌ Foydalanuvchilarni olishda xatolik yuz berdi.")

        # **State tugatamiz**
        await state.finish()
        