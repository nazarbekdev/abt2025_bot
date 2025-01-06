from aiogram.types import Message
from loader import dp, bot


@dp.message_handler(lambda message: message.text == "📊 Test Tahlili")
async def test_tahlili(message: Message):
    await message.answer("♻️ Tez orada ishga tushadi...")
