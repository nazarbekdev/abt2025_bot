from aiogram import types
from loader import dp, bot
from keyboards.button import test_buyurtma_kyb, main_kyb


@dp.message_handler(lambda message: message.text == "✍️ Test Yechish")
async def test_yechish(message: types.Message):
    await message.answer("Kerakli bo'limni tanlang", reply_markup=test_buyurtma_kyb.test_buyurtma_keyboard())


@dp.message_handler(lambda message: message.text == "🔙 Ortga Qaytish")
async def ortga_qaytish(message: types.Message):
    await message.answer("Asosiy bo'limdasiz.", reply_markup=main_kyb.main_keyboard())
