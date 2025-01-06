from aiogram import types
from aiogram.types import Message
from loader import dp, bot
from keyboards.inline import fanlar


@dp.message_handler(lambda message: message.text == "📝 Test Buyurtma")
async def test_buyurtma(message: types.Message):
    await message.answer("O'z sohangizni tanlang!", reply_markup=fanlar.fanlar_inline_keyboard())
