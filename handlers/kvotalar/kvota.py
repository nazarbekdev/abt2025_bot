from aiogram.types import Message
from loader import dp, bot


@dp.message_handler(lambda message: message.text == "🏛️ Kvotalar")
async def kvotalar(message: Message):
    await message.answer("2025-2026 o'quv yili uchun kvotalar hali e'lon qilinmadi!")
