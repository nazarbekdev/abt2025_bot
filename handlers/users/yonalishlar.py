from aiogram.types import Message
from loader import dp
from keyboards.inline.yonalishlar import yonalishlar_inline_keyboard


@dp.message_handler(lambda message: message.text == "🧑‍🎓 Yo'nalishlar")
async def yonalishlar(message: Message):
    await message.answer("Fanlar kesimi bo'yicha barcha yo'nalishlarni bilib oling!", reply_markup=yonalishlar_inline_keyboard())
    