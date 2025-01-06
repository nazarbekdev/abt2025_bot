from aiogram.types import Message
from loader import dp, bot
from keyboards.inline import tekshirish_usullari


@dp.message_handler(lambda message: message.text == "✅ Test Tekshirish")
async def test_tekshirish(message: Message):
    await message.answer("Qaysi usulda tekshirmoqchisiz?", reply_markup=tekshirish_usullari.tekshirish_usullari())
