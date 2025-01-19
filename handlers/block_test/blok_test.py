from aiogram.types import Message
from loader import dp, bot
from keyboards.button.blok_test import blok_test_keyboard


@dp.message_handler(lambda msg: msg.text == "📋 Blok test")
async def blok_test(message: Message):
    await message.answer("Blok test yechish uchun ro'yxatdan o'ting!", reply_markup=blok_test_keyboard())
