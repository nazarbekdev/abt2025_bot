from aiogram.types import Message
from loader import dp, bot
from keyboards.inline.dostlarni_taklif_qilish import taklif_qilish


@dp.message_handler(lambda message: message.text == "💰 Balans")
async def balans(message: Message):
    await message.answer("Siznig hisobingiz: 3000", reply_markup=taklif_qilish())
